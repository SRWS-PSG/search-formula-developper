"""Utilities for converting MEDLINE via Ovid search syntax to PubMed queries."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Callable, List, Match, Optional, Tuple

__all__ = [
    "FIELD_MAP",
    "ConvertResult",
    "OvidToPubMed",
    "convert_ovid_to_pubmed",
]

# ---------------------------------------------------------------------------
# Field mappings and helpers
# ---------------------------------------------------------------------------

FIELD_MAP = {
    "ti": "ti",
    "ab": "ab",
    "ti,ab": "tiab",
    "tw": "tiab",  # MEDLINE via Ovid treats .tw. as Title + Abstract
    "mp": "tw",
    "jn": "ta",
    "au": "au",
    "ad": "ad",
    "pt": "pt",
    "sh": "mh",
    "nm": "nm",
    "rn": "rn",
    "kf": "ot",
}

PROX_FIELD_PREF = ("tiab", "ti", "ad")
NO_QUOTE_TAGS = {"au", "pt", "ta"}


def _strip_outer_parentheses(text: str) -> str:
    text = text.strip()
    if not (text.startswith("(") and text.endswith(")")):
        return text

    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(text) - 1:
                return text
    return text[1:-1]


def _needs_quotes(term: str) -> bool:
    return bool(re.search(r"\s", term))


def _quote_if_needed(term: str) -> str:
    unquoted = term.strip('"')
    return f'"{unquoted}"' if _needs_quotes(unquoted) else unquoted


def _normalize_field_label(label: str) -> str:
    label = label.strip().lower()
    if label.startswith("."):
        label = label[1:]
    if label.endswith("."):
        label = label[:-1]
    return label


def _ovid_field_to_pubmed(label: str) -> Optional[str]:
    return FIELD_MAP.get(_normalize_field_label(label))


def _choose_prox_field(label: Optional[str]) -> str:
    preferred = _ovid_field_to_pubmed(label) if label else None
    if preferred in PROX_FIELD_PREF:
        return preferred
    return "tiab"


def _convert_wildcards(token: str, warnings: List[str]) -> str:
    output = token

    if re.search(r"\$\d+", output):
        output = re.sub(r"\$\d+", "*", output)
        warnings.append(
            "Ovidの数値付きトランケーション($n)はPubMedでは使用できないため'*'に変換しました。"
        )

    if output.endswith("$"):
        output = output[:-1] + "*"

    if "?" in output or "#" in output:
        output = output.replace("?", "*").replace("#", "*")
        warnings.append(
            "Ovidのワイルドカード('?','#')はPubMed非対応のため'*'に変換しました(ヒットが拡張される可能性あり)。"
        )

    for match in re.finditer(r"\b(\w{0,3})\*", output):
        if len(match.group(1)) < 4:
            warnings.append(
                f"PubMedでは語頭から4文字未満での'*'は無効になる可能性があります: '{match.group(0)}'"
            )
    return output


_MESH_RE = re.compile(
    r"""
    (?P<prefix>\*?\s*(?:exp\s+)?)
    (?P<term>"[^"]+"|[^()\s/]+(?:\s[^()/]+)*)
    /
    (?P<subhead>[A-Za-z]{2,}(?:\s[A-Za-z]+)?)?
    \.?
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _convert_mesh(match: Match[str]) -> str:
    prefix = match.group("prefix") or ""
    term = match.group("term").strip().strip('"')
    sub = match.group("subhead")

    is_focus = prefix.strip().startswith("*")
    is_expanded = "exp" in prefix

    mesh_tag = "majr" if is_focus else "mh"
    noexp = not is_expanded
    if is_focus and is_expanded:
        noexp = False

    if sub:
        noexp = False
        base = f"{term}/{sub}"
        return f"{base}[{mesh_tag}]"

    suffix = f"{mesh_tag}{'' if not noexp else ':noexp'}"
    return f"{term}[{suffix}]"


_ADJ_RE = re.compile(r"(?i)\badj\s*(\d+)\b")


def _convert_adjacent(phrase: str, label: Optional[str]) -> str:
    parts = re.split(_ADJ_RE, phrase)
    if len(parts) < 3:
        return phrase

    tokens = [parts[0].strip()]
    distance = parts[1]
    for index in range(2, len(parts), 2):
        tokens.append(parts[index].strip())

    field = _choose_prox_field(label)
    prox_terms = _quote_if_needed(" ".join(filter(None, tokens)))
    return f"{prox_terms}[{field}:~{distance}]"


def _format_leaf(token: str, tag: str, warnings: List[str], *, force_quotes: bool = False) -> str:
    stripped = token.strip()
    has_explicit_quotes = stripped.startswith('"') and stripped.endswith('"')
    core = stripped.strip('"') if has_explicit_quotes else stripped
    core = _convert_wildcards(core, warnings)

    if has_explicit_quotes:
        return f'"{core}"'
    if (force_quotes or _needs_quotes(core)) and tag not in NO_QUOTE_TAGS:
        return f'"{core}"'
    return core


def _apply_field(atom: str, label: str, warnings: List[str]) -> str:
    tag = _ovid_field_to_pubmed(label)
    if not tag:
        warnings.append(f"未対応のフィールド指定 '{label}' はそのまま残しました。")
        return atom

    if re.search(r"\[[^\]]+\]$", atom.strip()):
        return atom

    if re.search(_ADJ_RE, atom):
        return _convert_adjacent(atom, label)

    stripped = atom.strip()
    boolean_pattern = re.compile(r"\b(AND|OR|NOT)\b", re.IGNORECASE)
    if boolean_pattern.search(stripped):
        segments = re.split(r"(\bAND\b|\bOR\b|\bNOT\b)", atom, flags=re.IGNORECASE)
        rebuilt: List[str] = []
        for segment in segments:
            if segment is None:
                continue
            if not segment.strip():
                rebuilt.append(segment)
                continue
            if boolean_pattern.fullmatch(segment.strip()):
                rebuilt.append(segment.strip().upper())
                continue
            leading = segment[: len(segment) - len(segment.lstrip())]
            trailing = segment[len(segment.rstrip()):]
            token = segment.strip()
            formatted = _format_leaf(token, tag, warnings, force_quotes=True)
            rebuilt.append(f"{leading}{formatted}[{tag}]{trailing}")
        return "".join(rebuilt)

    formatted = _format_leaf(stripped, tag, warnings)
    return f"{formatted}[{tag}]"


def _replace_iter(text: str, pattern: re.Pattern[str], repl: Callable[[Match[str]], str]) -> str:
    while True:
        match = pattern.search(text)
        if not match:
            break
        replacement = repl(match)
        text = text[: match.start()] + replacement + text[match.end():]
    return text


@dataclass
class ConvertResult:
    query: str
    warnings: List[str]


class OvidToPubMed:
    """Convert Ovid syntax into PubMed query language."""

    def convert(self, ovid_query: str) -> ConvertResult:
        text = ovid_query.strip()
        warnings: List[str] = []

        text = _MESH_RE.sub(_convert_mesh, text)

        group_pattern = re.compile(r"(\([^()]+\))\s*(\.[A-Za-z,]+\.)", re.IGNORECASE)
        def _replace_group(match: Match[str]) -> str:
            inner = _strip_outer_parentheses(match.group(1))
            label = match.group(2)
            converted_inner = _apply_field(inner, label, warnings)
            if re.search(r"\b(AND|OR|NOT)\b", converted_inner, re.IGNORECASE):
                return f"({converted_inner})"
            return converted_inner

        text = _replace_iter(text, group_pattern, _replace_group)

        atom_pattern = re.compile(
            r'(?<!\[)[\w*"#\-\?]+(?:\s[\w*"#\-\?]+)*\s*(\.[A-Za-z,]+\.)',
            re.IGNORECASE,
        )

        def _replace_atom(match: Match[str]) -> str:
            full = match.group(0)
            label = match.group(1)
            atom = full[: -len(label)].strip()
            return _apply_field(atom, label, warnings)

        text = _replace_iter(text, atom_pattern, _replace_atom)

        loose_adj_pattern = re.compile(
            r"([^(\s]+(?:\s+[^)\s]+)*)\s+adj\s*(\d+)\s+([^(\s]+(?:\s+[^)\s]+)*)",
            re.IGNORECASE,
        )

        def _replace_loose_adj(match: Match[str]) -> str:
            left, distance, right = match.groups()
            prox_terms = _quote_if_needed(f"{left} {right}")
            return f"{prox_terms}[tiab:~{distance}]"

        text = _replace_iter(text, loose_adj_pattern, _replace_loose_adj)

        def _maybe_convert(token: str) -> str:
            if re.search(r"\[[^\]]+\]$", token):
                return token
            return _convert_wildcards(token, warnings)

        tokens = re.split(r"(\s+|\(|\)|AND|OR|NOT)", text, flags=re.IGNORECASE)
        rebuilt: List[str] = []
        for token in tokens:
            if not token or token.isspace():
                rebuilt.append(token)
                continue
            if token in {"(", ")"} or re.fullmatch(r"AND|OR|NOT", token, re.IGNORECASE):
                rebuilt.append(token)
                continue
            rebuilt.append(_maybe_convert(token))

        text = "".join(rebuilt)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"\b(and|or|not)\b", lambda m: m.group(1).upper(), text, flags=re.IGNORECASE)

        return ConvertResult(query=text, warnings=warnings)


def convert_ovid_to_pubmed(ovid_query: str) -> Tuple[str, List[str]]:
    result = OvidToPubMed().convert(ovid_query)
    return result.query, result.warnings
