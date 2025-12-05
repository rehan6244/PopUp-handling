# tests/test_price_consistency.py
from lufthansa_challenges.price_consistency_checker import validate_price_breakdown

def test_real_production_bug():
    bad_breakdown = {
        "baseFare": 199.00,
        "taxes": 98.00,
        "carrierSurcharge": 50.00,
        "total": 346.99  # should be 347.00
    }
    assert validate_price_breakdown(bad_breakdown) is False

def test_valid_price():
    good = {
        "baseFare": 299.00,
        "taxes": 127.50,
        "carrierSurcharge": 45.00,
        "total": 471.50
    }
    assert validate_price_breakdown(good) is True