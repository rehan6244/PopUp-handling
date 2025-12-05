# unit tests/test_baggage_rules.py
from lufthansa_challenges.intermediate_baggage_rules import get_baggage_allowance

def test_intercontinental_business_class():
    result = get_baggage_allowance("Business", "FRA", "JFK")
    assert result["checked_baggage"] == "3 pieces up to 32 kg each"
    assert result["hand_baggage"] == "1 x 8kg"

def test_domestic_economy():
    result = get_baggage_allowance("Economy", "MUC", "BER")
    assert result["checked_baggage"] == "No free checked baggage"

def test_excess_baggage_detection():
    from lufthansa_challenges.intermediate_baggage_rules import is_baggage_excess
    excess, msg = is_baggage_excess(bags=3, weight_per_bag=25, origin="FRA", destination="JFK", cabin="Economy")
    assert excess is True
    assert "Too many pieces" in msg