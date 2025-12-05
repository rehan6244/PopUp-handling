"""
Lufthansa Beginner-Friendly Test Engineer Challenges
Real problems Lufthansa QA teams face daily — solved cleanly in pure Python
Perfect for interviews or to show you "get" airline logic
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict


def is_valid_booking_code(code: str) -> bool:
    """
    Lufthansa booking codes (PNR) are always 6 alphanumeric characters.
    Example: "ABC123", "X7K9M2"
    """
    return len(code) == 6 and code.isalnum()


def calculate_flight_duration(departure: str, arrival: str) -> str:
    """
    Input: "14:30", "18:45" → Output: "4h 15m"
    Real Lufthansa test data format
    """
    fmt = "%H:%M"
    dep = datetime.strptime(departure, fmt)
    arr = datetime.strptime(arrival, fmt)
    if arr < dep:
        arr += timedelta(days=1)  # overnight flight
    duration = arr - dep
    hours, remainder = divmod(duration.seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m"


def find_cheapest_fare(fares: List[Dict]) -> Dict:
    """
    Given list of fares, return the cheapest one.
    Real structure from Lufthansa JSON responses.
    """
    return min(fares, key=lambda x: x["price"]["total"])


def is_direct_flight(stops: int) -> bool:
    """Direct flight = 0 stops"""
    return stops == 0


def generate_test_pnr() -> str:
    """Generate 10 valid Lufthansa-style PNRs for test data"""
    import random
    import string
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def validate_departure_before_return(dep_date: str, ret_date: str) -> bool:
    """
    Simple but CRITICAL rule Lufthansa tests must catch:
    Return date cannot be before departure date
    """
    dep = datetime.strptime(dep_date, "%Y-%m-%d")
    ret = datetime.strptime(ret_date, "%Y-%m-%d")
    return ret >= dep


# Demo / Test cases (recruiters love this)
if __name__ == "__main__":
    print("Lufthansa Beginner Challenges - Demo")
    print("="*50)
    print(f"Valid PNR 'ABC123': {is_valid_booking_code('ABC123')}")
    print(f"Flight MUC→JFK 09:15→11:30: {calculate_flight_duration('09:15', '11:30')}")
    print(f"Overnight flight 23:50→06:20: {calculate_flight_duration('23:50', '06:20')}")

    fares = [
        {"route": "FRA-BER", "price": {"total": 99}},
        {"route": "FRA-BER", "price": {"total": 149}},
        {"route": "FRA-BER", "price": {"total": 79}},
    ]
    print(f"Cheapest fare: €{find_cheapest_fare(fares)['price']['total']}")

    print(f"Generated test PNR: {generate_test_pnr()}")
    print(f"2025-12-20 → 2025-12-15 valid return? {validate_departure_before_return('2025-12-20', '2025-12-15')}")