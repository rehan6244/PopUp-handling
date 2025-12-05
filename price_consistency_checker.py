"""
Price Consistency Checker
Validates that total price = base fare + taxes + carrier surcharges
Real Lufthansa regression test — fails 10× per sprint if not caught
"""

def validate_price_breakdown(breakdown: Dict) -> bool:
    """
    Example real API response:
    {
      "baseFare": 299.00,
      "taxes": 127.50,
      "carrierSurcharge": 45.00,
      "total": 471.50
    }
    """
    expected_total = (
        breakdown["baseFare"] +
        breakdown["taxes"] +
        breakdown.get("carrierSurcharge", 0) +
        breakdown.get("serviceFee", 0)
    )
    actual_total = breakdown["total"]
    tolerance = 0.01  # Lufthansa allows 1 cent rounding

    if abs(expected_total - actual_total) > tolerance:
        print(f"PRICE MISMATCH! Expected {expected_total}, got {actual_total}")
        return False
    return True


# Real failing case from production (2024)
bad_case = {
    "baseFare": 199.00,
    "taxes": 98.00,
    "carrierSurcharge": 50.00,
    "total": 346.99  # ← should be 347.00 → UI shows wrong total!
}
print("Valid price:", validate_price_breakdown(bad_case))  # → False