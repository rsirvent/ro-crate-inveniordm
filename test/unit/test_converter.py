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
