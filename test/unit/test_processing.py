import mapping.processing_functions as pf

def test_dateProcessing():
    out = pf.dateProcessing("5 June 2012")

    assert out == "2012-06-05"
