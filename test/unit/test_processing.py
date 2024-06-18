import mapping.processing_functions as pf
import pytest


def test_dateProcessing__date_only():
    out = pf.dateProcessing("5 June 2012")

    assert out == "2012-06-05"


def test_dateProcessing__timestamp():
    out = pf.dateProcessing("5 June 2012 09:30:44")

    assert out == "2012-06-05"


def test_dateProcessing__year_only():
    out = pf.dateProcessing("2012")

    assert out == "2012"


def test_dateProcessing__empty():
    out = pf.dateProcessing("")

    assert out is None


def test_dateProcessing__none():
    out = pf.dateProcessing(None)

    assert out is None
