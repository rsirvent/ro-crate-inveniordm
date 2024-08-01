import re

import pytest

import rocrate_inveniordm.mapping.crate_utils as cu
import rocrate_inveniordm.mapping.mapping_utils as mu
from test.unit.utils import (
    load_template_rc,
    set_field_in_template_rde,
)

MINIMAL_CRATE_PATH = "test/data/minimal-ro-crate/ro-crate-metadata.json"
TEST_REFERENCING_CRATE_PATH = (
    "test/data/test-referencing-ro-crate/ro-crate-metadata.json"
)

EXPECTED_REFERENCE_ENTITIES: dict[str, dict] = {
    "license": {
        "@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
        "@type": "CreativeWork",
        "description": (
            "This work is licensed under the Creative Commons "
            "Attribution-NonCommercial-ShareAlike 3.0 Australia License. To view a "
            "copy of this license, visit "
            "http://creativecommons.org/licenses/by-nc-sa/3.0/au/ or send a letter to "
            "Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."
        ),
        "identifier": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/",
        "name": (
            "Attribution-NonCommercial-ShareAlike 3.0 Australia (CC BY-NC-SA 3.0 AU)"
        ),
    },
    "author": {
        "@id": "https://orcid.org/0009-0001-3915-5910",
        "@type": "Person",
        "givenName": "Milan",
        "familyName": "Szente",
        "affiliation": {"@id": "https://ror.org/04d836q62"},
    },
    "publisher": {
        "@id": "https://ror.org/04d836q62",
        "@type": ["Organization", "CollegeOrUniversity"],
        "name": "TU Wien",
    },
}


def test_dereference_string():
    rc = load_template_rc(MINIMAL_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    expected = "2017"

    result = cu.dereference(rc, rde, "datePublished")

    assert result == expected


def test_dereference_entity():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    expected = EXPECTED_REFERENCE_ENTITIES["license"]

    result = cu.dereference(rc, rde, "$license")

    assert result == expected


def test_dereference_string_array_item():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    expected = "text/plain"

    result = cu.dereference(rc, rde, "encodingFormat", 1)

    assert result == expected


def test_dereference_entity_array_item():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    expected = EXPECTED_REFERENCE_ENTITIES["author"]

    result = cu.dereference(rc, rde, "$author", 1)

    assert result == expected


def test_rc_get_rde():
    rc = load_template_rc(MINIMAL_CRATE_PATH)
    expected = {
        "@id": "./",
        "identifier": "https://doi.org/10.4225/59/59672c09f4a4b",
        "@type": "Dataset",
        "datePublished": "2017",
        "name": (
            "Data files associated with the manuscript:Effects of facilitated "
            "family case conferencing for ..."
        ),
        "description": (
            "Palliative care planning for nursing home residents with "
            "advanced dementia ..."
        ),
        "license": {"@id": "https://creativecommons.org/licenses/by-nc-sa/3.0/au/"},
    }

    result = cu.rc_get_rde(rc)

    assert result == expected


@pytest.mark.parametrize(
    ["key", "path", "expected"],
    [
        # # single-part key
        # string
        ("datePublished", [], "2023-02-02"),
        # entity
        ("$license", [], EXPECTED_REFERENCE_ENTITIES["license"]),
        # array item - string
        ("encodingFormat[]", [1], "text/plain"),
        # whole array
        ("encodingFormat[]", [-1], ["text/csv", "text/plain"]),
        # array item - entity
        ("$author[]", [1], EXPECTED_REFERENCE_ENTITIES["author"]),
        # # multiple-part key
        # property on entity
        (
            "$license.name",
            [],
            EXPECTED_REFERENCE_ENTITIES["license"]["name"],
        ),
        # property on entity within array
        (
            "$author[].givenName",
            [1],
            EXPECTED_REFERENCE_ENTITIES["author"]["givenName"],
        ),
        # entity referenced by entity within array
        (
            "$author[].$affiliation",
            [1],
            EXPECTED_REFERENCE_ENTITIES["publisher"],
        ),
        # array element within property on entity
        (
            "$publisher.@type[]",
            [1],
            "CollegeOrUniversity",
        ),
        # nested arrays - multiple-step path
        (
            "$contentLocation[].@type[]",
            [0, 1],
            "Park",
        ),
        # # three-step key
        (
            "$author[].$affiliation.name",
            [1],
            EXPECTED_REFERENCE_ENTITIES["publisher"]["name"],
        ),
    ],
)
def test_get_value_from_rc__succeeds(key: str, path: list | None, expected: dict | str):
    """For each key and path combination, verifies that the retrieved entity matches
    what is expected."""
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)

    result = cu.get_value_from_rc(rc, key, path)

    assert result == expected


@pytest.mark.parametrize(
    ["key", "path"],
    [
        # empty key
        ("", []),
        # invalid keys
        ("test", []),
        ("$test", []),
        ("test[]", [0]),
    ],
)
def test_get_value_from_rc__none(key, path):
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)

    result = cu.get_value_from_rc(rc, key, path)

    assert result is None


@pytest.mark.parametrize(
    ["key", "path", "expected_error", "expected_message"],
    [
        # invalid key
        (
            "$test[]",
            [0],
            ValueError,
            "Value of $test is not a list, but an index was provided.",
        ),
        # invalid index / path format
        ("author[]", [], IndexError, "out of range"),
        ("$author[]", [], IndexError, "out of range"),
        ("author[]", [2], IndexError, "out of range"),
        ("$author[]", [2], IndexError, "out of range"),
        ("$author[]", ["value"], TypeError, "list indices must be integers or slices"),
        ("$author[]", "value", TypeError, "list indices must be integers or slices"),
    ],
)
def test_get_value_from_rc__error(key, path, expected_error, expected_message):
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)

    with pytest.raises(expected_error, match=re.escape(expected_message)):
        cu.get_value_from_rc(rc, key, path)


def test_get_referenced_entity__direct():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    expected = EXPECTED_REFERENCE_ENTITIES["license"]

    result = cu.get_referenced_entity(rc, rde, "$license")

    assert result == expected


def test_get_referenced_entity__array_item():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    expected = EXPECTED_REFERENCE_ENTITIES["author"]

    result = cu.get_referenced_entity(rc, rde, "$author", 1)

    assert result == expected


def test_get_referenced_entity__nonexistent_key():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)

    result = cu.get_referenced_entity(rc, rde, "$test")

    assert result is None


def test_get_referenced_entity__fails_key_format():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    key = "license"

    with pytest.raises(mu.MappingException, match=re.escape("$-prefixed key expected")):
        cu.get_referenced_entity(rc, rde, key)


def test_get_referenced_entity__fails_list_no_index():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    rde = cu.rc_get_rde(rc)
    key = "$author"

    with pytest.raises(
        ValueError,
        match=re.escape(f"Value of {key} is a list, but no index was provided."),
    ):
        cu.get_referenced_entity(rc, rde, key)


def test_get_referenced_entity__id_not_in_crate():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    parent_entity = {
        "@type": "CreativeWork",
        "@id": "ro-crate-metadata.json",
        "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
        "about": {"@id": "./"},
    }
    key = "$conformsTo"

    result = cu.get_referenced_entity(rc, parent_entity, key)

    assert result is None


def test_get_referenced_entity_from_root():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    key = "$license"
    expected = EXPECTED_REFERENCE_ENTITIES["license"]

    result = cu.get_referenced_entity_from_root(rc, key)

    assert result == expected


def test_get_referenced_entity_from_root__key_not_in_rde(capsys):
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    key = "$conformsTo"

    result = cu.get_referenced_entity_from_root(rc, key)

    assert result is None
    captured = capsys.readouterr()
    assert "not found in RO-Crate Root Data Entity" in captured.out


def test_get_referenced_entity_from_root__id_not_in_crate(capsys):
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    key = "$test"
    value = {"@id": "https://example.org"}
    set_field_in_template_rde(key[1:], value, rc)

    result = cu.get_referenced_entity_from_root(rc, key)
    assert result is None
    captured = capsys.readouterr()
    assert "not found in RO-Crate Root Data Entity" not in captured.out


def test_get_referenced_entity_from_root__fails_key_format():
    rc = load_template_rc(TEST_REFERENCING_CRATE_PATH)
    key = "license"

    with pytest.raises(mu.MappingException, match=re.escape("$-prefixed key expected")):
        cu.get_referenced_entity_from_root(rc, key)
