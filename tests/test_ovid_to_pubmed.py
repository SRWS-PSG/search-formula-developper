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
