# tests/api/test_baggage_in_api_response.py
def test_baggage_allowance_in_search_response():
    from lufthansa_challenges.intermediate_baggage_rules import get_baggage_allowance
    
    expected = get_baggage_allowance("Business", "FRA", "JFK")
    assert expected["checked_baggage"] == "3 pieces up to 32 kg each"
    
    # Simulate API response
    api_response = {
        "cabinClass": "BUSINESS",
        "origin": "FRA",
        "destination": "JFK",
        "baggage": {
            "checked": "3 pieces up to 32 kg each",
            "hand": "1 x 8kg"
        }
    }
    
    assert api_response["baggage"]["checked"] == expected["checked_baggage"]