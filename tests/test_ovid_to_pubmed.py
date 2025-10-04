"""Tests for the Ovid to PubMed conversion utilities."""

import pytest

from scripts.conversion.ovid.converter import convert_ovid_to_pubmed


@pytest.mark.parametrize(
    ("ovid", "expected"),
    [
        ("asthma.ti.", "asthma[ti]"),
        ("asthma.ab.", "asthma[ab]"),
        ("asthma.ti,ab.", "asthma[tiab]"),
        ('"heart failure".ti,ab.', '"heart failure"[tiab]'),
        ("poisoning.tw.", "poisoning[tiab]"),
        ("tamiflu.mp.", "tamiflu[tw]"),
        ("exp Asthma/.", "Asthma[mh]"),
        ("Asthma/.", "Asthma[mh:noexp]"),
        ("*Asthma/.", "Asthma[majr:noexp]"),
        ("*exp Asthma/.", "Asthma[majr]"),
        ("Neoplasms/dh.", "Neoplasms/dh[mh]"),
        ("Neoplasms/diet therapy.", "Neoplasms/diet therapy[mh]"),
        (("(heart adj3 failure).ti,ab."), '"heart failure"[tiab:~3]'),
        (
            "(patient adj0 physician adj0 relationship).ti,ab.",
            '"patient physician relationship"[tiab:~0]',
        ),
        ("Nature.jn.", "Nature[ta]"),
        ("Smith JA.au.", "Smith JA[au]"),
        ("Aspirin.nm.", "Aspirin[nm]"),
        ("50-78-2.rn.", "50-78-2[rn]"),
    ],
)
def test_basic_mappings(ovid: str, expected: str) -> None:
    query, warnings = convert_ovid_to_pubmed(ovid)
    assert query == expected
    assert warnings == []


def test_group_with_field_and_boolean() -> None:
    query, warnings = convert_ovid_to_pubmed(
        '(influenza or "common cold").ti,ab. and randomized controlled trial.pt.'
    )
    assert (
        query
        == '("influenza"[tiab] OR "common cold"[tiab]) AND randomized controlled trial[pt]'
    )
    assert warnings == []


def test_adj_without_field_defaults_tiab() -> None:
    query, warnings = convert_ovid_to_pubmed("heart adj4 failure")
    assert query == '"heart failure"[tiab:~4]'
    assert warnings == []


def test_mesh_focus_and_explode_combinations() -> None:
    query_focus_explode, _ = convert_ovid_to_pubmed("*exp Diabetes Mellitus/.")
    query_focus, _ = convert_ovid_to_pubmed("*Diabetes Mellitus/.")
    query_plain, _ = convert_ovid_to_pubmed("Diabetes Mellitus/.")
    assert query_focus_explode == "Diabetes Mellitus[majr]"
    assert query_focus == "Diabetes Mellitus[majr:noexp]"
    assert query_plain == "Diabetes Mellitus[mh:noexp]"


def test_wildcard_notes_and_expansion() -> None:
    query, warnings = convert_ovid_to_pubmed("p?ediatric.ti,ab.")
    assert query == "p*ediatric[tiab]"
    assert any("非対応" in warning for warning in warnings)


def test_truncation_minlen_warning() -> None:
    query, warnings = convert_ovid_to_pubmed("cov*.tw.")
    assert query == "cov*[tiab]"
    assert any("4文字未満" in warning for warning in warnings)


def test_field_ti_ab_kw_mapping() -> None:
    query, warnings = convert_ovid_to_pubmed("colonoscopy.ti,ab,kw.")
    assert query == "colonoscopy[tiab]"
    assert warnings == []


def test_field_tw_kw_mapping() -> None:
    query, warnings = convert_ovid_to_pubmed("endoscopy.tw,kw.")
    assert query == "endoscopy[tiab]"
    assert warnings == []


def test_adj_with_or_in_parentheses() -> None:
    query, warnings = convert_ovid_to_pubmed("(narrow adj3 band).ti,ab.")
    assert query == '"narrow band"[tiab:~3]'
    assert warnings == []


def test_adj_with_or_options_right() -> None:
    query, warnings = convert_ovid_to_pubmed("(linked adj3 (color or colour)).ti,ab.")
    assert query == '("linked color"[tiab:~3] OR "linked colour"[tiab:~3])'
    assert warnings == []


def test_adj_with_or_options_both_sides() -> None:
    query, warnings = convert_ovid_to_pubmed("((color or colour) adj3 (enhance* or imag*)).ti,ab.")
    expected = (
        '("color enhance*"[tiab:~3] OR "color imag*"[tiab:~3] OR '
        '"colour enhance*"[tiab:~3] OR "colour imag*"[tiab:~3])'
    )
    assert query == expected
    assert warnings == []


def test_complex_boolean_with_adj_in_parens() -> None:
    query, warnings = convert_ovid_to_pubmed("((narrow adj3 band) or NBI).ti,ab,kw.")
    assert query == '("narrow band"[tiab:~3] OR "NBI"[tiab])'
    assert warnings == []


def test_multiple_adj_with_or_in_boolean() -> None:
    query, warnings = convert_ovid_to_pubmed(
        "((blue adj3 (laser or light)) or BLI).ti,ab,kw."
    )
    expected = '(("blue laser"[tiab:~3] OR "blue light"[tiab:~3]) OR "BLI"[tiab])'
    assert query == expected
    assert warnings == []


def test_wildcard_in_adj_with_or() -> None:
    query, warnings = convert_ovid_to_pubmed(
        "((textur* adj3 (color or colour)) or TXI).ti,ab,kw."
    )
    expected = '(("textur* color"[tiab:~3] OR "textur* colour"[tiab:~3]) OR "TXI"[tiab])'
    assert query == expected
    assert len(warnings) > 0


def test_complex_nested_adj_pattern() -> None:
    query, warnings = convert_ovid_to_pubmed(
        "((fujinon adj3 (intelligent* or color or colour)) or FICE).ti,ab,kw."
    )
    expected = (
        '(("fujinon intelligent*"[tiab:~3] OR "fujinon color"[tiab:~3] OR '
        '"fujinon colour"[tiab:~3]) OR "FICE"[tiab])'
    )
    assert query == expected
    assert warnings == []
