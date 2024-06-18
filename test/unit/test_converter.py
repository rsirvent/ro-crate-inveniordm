import mapping.converter as converter
import pytest
import re


def test_check_condition__true():
    rule = "?string"
    value = "This is a string"

    result = converter.check_condition(rule, value)

    assert result


def test_check_condition__false():
    rule = "?string"
    value = 3

    result = converter.check_condition(rule, value)

    assert not result


def test_check_condition__incorrect_format():
    rule = "string"
    value = "This is a string"

    with pytest.raises(
        ValueError, match=re.escape(f"Condition rule {rule} must start with ?")
    ):
        converter.check_condition(rule, value)


def test_check_condition__nonexistent():
    rule = "?random"
    value = "This is a string"

    with pytest.raises(
        NotImplementedError, match=re.escape(f"Function {rule} not implemented.")
    ):
        converter.check_condition(rule, value)


def test_process__valid():
    rule = "$dateProcessing"
    value = "18 June 2024"

    result = converter.process(rule, value)

    assert result == "2024-06-18"


def test_process__empty():
    rule = "$dateProcessing"
    value = ""

    result = converter.process(rule, value)

    assert result is None


def test_process__incorrect_format():
    rule = "dateProcessing"
    value = "18 June 2024"

    with pytest.raises(
        ValueError, match=re.escape(f"Processing rule {rule} must start with $")
    ):
        converter.process(rule, value)


def test_process__nonexistent():
    rule = "$date"
    value = "18 June 2024"

    with pytest.raises(
        NotImplementedError, match=re.escape(f"Function {rule} not implemented.")
    ):
        converter.process(rule, value)


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

    result = converter.setup_dc()

    assert result == expected
