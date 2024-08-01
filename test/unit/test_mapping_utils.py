import json
import re

import pytest

import rocrate_inveniordm.mapping.mapping_utils as mu


def test_raise_mappingexception():
    with pytest.raises(
        mu.MappingException,
        match=re.escape("The loaded mapping is invalid: test message"),
    ):
        raise mu.MappingException("test message")


def test_load_mapping_json():
    with open("src/rocrate_inveniordm/mapping/mapping.json") as f:
        expected_json = json.load(f)

    result_json = mu.load_mapping_json()

    assert result_json == expected_json


def test_get_arrays_from_from_values():
    input = [
        "name",
        "$author[].$affiliation[].name",
        "$license[]",
        "$publisher.name",
        "keywords[]",
    ]
    expected = {"$author[].$affiliation[]", "$license[]", "keywords[]"}

    result = mu.get_arrays_from_from_values(input)

    assert set(result) == expected


def test_contains_atatthis__string_true():
    assert mu.contains_atatthis("@@this") is True


def test_contains_atatthis__string_false():
    assert mu.contains_atatthis("other string") is False


def test_contains_atatthis__dict_first_item():
    input = {
        "test": "@@this",
        "other": "other string",
    }

    assert mu.contains_atatthis(input) is True


@pytest.mark.xfail(reason="uncertain on intended design of function. TODO review this")
def test_contains_atatthis__dict_later_item():
    input = {
        "other": "other string",
        "test": "@@this",
    }

    assert mu.contains_atatthis(input) is True


def test_contains_atatthis__dict_nested():
    input = {
        "test": {"subtest": "@@this"},
        "other": "other string",
    }

    assert mu.contains_atatthis(input) is True


def test_contains_atatthis__dict_false():
    input = {
        "other": "other string",
        "test": "this",
    }
    assert mu.contains_atatthis(input) is False


def test_contains_atatthis__unsupported_type():
    input = ["@@this"]

    assert mu.contains_atatthis(input) is False


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        ("author", "author"),
        ("author[]", "author"),
        ("$author", "author"),
        ("$author[]", "author"),
        ("$author[].name", "author.name"),
    ],
)
def test_clean_key(input, expected):
    result = mu.clean_key(input)

    assert result == expected


def test_format_value__str():
    input = "test @@this"
    value = "insert"
    result = mu.format_value(input, value)

    assert result == "test insert"


def test_format_value__dict():
    input = {"test": "@@this", "second test": "also @@this", "consistent": "consistent"}
    value = "insert"
    expected = {
        "test": "insert",
        "second test": "also insert",
        "consistent": "consistent",
    }

    result = mu.format_value(input, value)

    assert result == expected


def test_format_value__bool():
    input = True
    value = "insert"

    result = mu.format_value(input, value)

    assert result is True


def test_format_value__unsupported_type():
    input = ["@@this"]
    value = "insert"

    with pytest.raises(
        TypeError,
        match=re.escape(
            f"Format must be a string, dictionary, or bool, but is {type(input)}."
        ),
    ):
        mu.format_value(input, value)


def test_format_value__nothing_to_do():
    input = "test consistent"
    value = "insert"
    result = mu.format_value(input, value)

    assert result == "test consistent"


def test_setup_dc():
    expected = {
        "access": {
            "record": "public",  # public or restricted; 1
            "files": "public",  # public or restricted; 1
            "embargo": {"active": False},  # 0-1
        },
        "metadata": {},
        "files": {"enabled": True},
    }

    result = mu.setup_dc()

    assert result == expected
