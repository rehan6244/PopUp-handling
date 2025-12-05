# tests/test_fare_rules.py
from lufthansa_challenges.advanced_fare_rules import get_fare_benefits, is_flex_fare

def test_economy_light_no_rebooking():
    benefits = get_fare_benefits("Economy Light")
    assert benefits["rebooking"] == "not permitted"
    assert benefits["checked_baggage"] == "not included (extra fee)"

def test_flex_fare_benefits():
    assert is_flex_fare("Economy Flex") is True
    assert is_flex_fare("Business Flex") is True
    assert is_flex_fare("Economy Classic") is False