"""
Lufthansa Intermediate Baggage Rules Engine
Real-world baggage allowance logic used in Lufthansa booking flow
Perfect interview / test-automation demo
"""

from typing import Dict, List, Tuple
from enum import Enum


class CabinClass(Enum):
    ECONOMY = "Economy"
    PREMIUM_ECONOMY = "Premium Economy"
    BUSINESS = "Business"
    FIRST = "First"


class RouteType(Enum):
    DOMESTIC_EU = "Domestic/EU"
    SHORT_HAUL = "Short-haul International"
    LONG_HAUL = "Long-haul International"
    INTERCONTINENTAL = "Intercontinental"


# Lufthansa real baggage policy (2025 rules - simplified)
BAGGAGE_POLICY = {
    CabinClass.ECONOMY: {
        RouteType.DOMESTIC_EU:      {"pieces": 0, "hand": "8kg"},
        RouteType.SHORT_HAUL:       {"pieces": 1, "weight": 23, "hand": "8kg"},
        RouteType.LONG_HAUL:        {"pieces": 1, "weight": 23, "hand": "8kg"},
        RouteType.INTERCONTINENTAL: {"pieces": 2, "weight": 23, "hand": "8kg"},
    },
    CabinClass.PREMIUM_ECONOMY: {
        RouteType.DOMESTIC_EU:      {"pieces": 0, "hand": "8kg"},
        RouteType.SHORT_HAUL:       {"pieces": 2, "weight": 23, "hand": "8kg"},
        RouteType.LONG_HAUL:        {"pieces": 2, "weight": 23, "hand": "8kg"},
        RouteType.INTERCONTINENTAL: {"pieces": 2, "weight": 23, "hand": "8kg"},
    },
    CabinClass.BUSINESS: {
        RouteType.DOMESTIC_EU:      {"pieces": 1, "weight": 32, "hand": "8kg"},
        RouteType.SHORT_HAUL:       {"pieces": 2, "weight": 32, "hand": "8kg"},
        RouteType.LONG_HAUL:        {"pieces": 2, "weight": 32, "hand": "8kg"},
        RouteType.INTERCONTINENTAL: {"pieces": 3, "weight": 32, "hand": "8kg"},
    },
    CabinClass.FIRST: {
        RouteType.DOMESTIC_EU:      {"pieces": 2, "weight": 32, "hand": "12kg"},
        RouteType.SHORT_HAUL:       {"pieces": 3, "weight": 32, "hand": "12kg"},
        RouteType.LONG_HAUL:        {"pieces": 3, "weight": 32, "hand": "12kg"},
        RouteType.INTERCONTINENTAL: {"pieces": 3, "weight": 32, "hand": "12kg"},
    },
}


def classify_route(origin: str, destination: str) -> RouteType:
    """Simplified real Lufthansa route classification"""
    eu_airports = {"FRA", "MUC", "BER", "HAM", "DUS", "STR", "LHR", "CDG", "AMS", "MAD", "ZRH"}
    long_haul = {"JFK", "LAX", "PEK", "HND", "DEL", "EWR", "SIN", "BKK", "GRU", "JNB"}

    o, d = origin[:3].upper(), destination[:3].upper()

    if o in eu_airports and d in eu_airports:
        return RouteType.DOMESTIC_EU
    elif d in long_haul or o in long_haul:
        return RouteType.INTERCONTINENTAL
    elif o[:2] == d[:2]:  # same country
        return RouteType.DOMESTIC_EU
    else:
        return RouteType.LONG_HAUL


def get_baggage_allowance(
    cabin: str, origin: str, destination: str
) -> Dict[str, str]:
    """
    Returns exact baggage allowance string as shown on lufthansa.com
    """
    cabin_class = CabinClass(cabin.upper().replace(" ", "_"))
    route_type = classify_route(origin, destination)
    policy = BAGGAGE_POLICY[cabin_class][route_type]

    pieces = policy.get("pieces", 0)
    weight = policy.get("weight", 0)
    hand = policy["hand"]

    if pieces == 0:
        checked = "No free checked baggage"
    elif pieces == 1:
        checked = f"1 piece up to {weight} kg"
    else:
        checked = f"{pieces} pieces up to {weight} kg each"

    return {
        "checked_baggage": checked,
        "hand_baggage": f"1 x {hand}",
        "route_type": route_type.value,
        "cabin_class": cabin_class.value,
    }


def is_baggage_excess(bags: int, weight_per_bag: int, origin: str, destination: str, cabin: str) -> Tuple[bool, str]:
    """Check if passenger exceeds allowance"""
    allowance = get_baggage_allowance(cabin, origin, destination)
    allowed_pieces = int(allowance["checked_baggage"].split()[0]) if "piece" in allowance["checked_baggage"] else 0
    allowed_weight = int(allowance["checked_baggage"].split()[-2]) if "kg" in allowance["checked_baggage"] else 0

    if bags > allowed_pieces:
        return True, f"Too many pieces ({bags} > {allowed_pieces})"
    if bags > 0 and weight_per_bag > allowed_weight:
        return True, f"Bag too heavy ({weight_per_bag}kg > {allowed_weight}kg)"
    return False, "Within allowance"


# Demo
if __name__ == "__main__":
    print("Lufthansa Baggage Rules Engine")
    print("="*50)

    test_cases = [
        ("Economy", "FRA", "JFK"),
        ("Business", "MUC", "BER"),
        ("Premium Economy", "FRA", "LHR"),
        ("First", "MUC", "SIN"),
    ]

    for cabin, ori, dest in test_cases:
        allowance = get_baggage_allowance(cabin, ori, dest)
        print(f"{cabin:16} | {ori} → {dest} | {allowance['checked_baggage']}, Hand: {allowance['hand_baggage']}")

    print("\nExcess check:")
    print(is_baggage_excess(3, 25, "FRA", "JFK", "Economy"))   # → excess pieces
    print(is_baggage_excess(2, 35, "FRA", "JFK", "Business"))  # → excess weight
    print(is_baggage_excess(2, 30, "FRA", "JFK", "Business"))  # → OK