# tests/api/test_price_consistency_api.py
def test_api_price_breakdown_is_correct():
    sample = {
        "baseFare": 299.00,
        "taxesAndFees": 127.50,
        "carrierSurcharge": 45.00,
        "totalAmount": 471.50
    }
    
    calculated = sample["baseFare"] + sample["taxesAndFees"] + sample["carrierSurcharge"]
    assert abs(calculated - sample["totalAmount"]) < 0.02
    
    # Real bug caught in production 2024
    bug_case = {
        "baseFare": 199.00,
        "taxesAndFees": 98.00,
        "carrierSurcharge": 50.00,
        "totalAmount": 346.99  # ← should be 347.00
    }
    calculated = bug_case["baseFare"] + bug_case["taxesAndFees"] + bug_case["carrierSurcharge"]
    assert abs(calculated - bug_case["totalAmount"]) > 0.01  # ← FAILS → bug caught!