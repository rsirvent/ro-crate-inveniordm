import mapping.condition_functions as cf

def test_is_uri():
    input = "https://example.org"
    
    assert cf.is_uri(input)
