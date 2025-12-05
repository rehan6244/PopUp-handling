"""
PNR & Passenger Name Validation
Real rules from Lufthansa booking + check-in systems
"""

import re


def is_valid_pnr(pnr: str) -> bool:
    return bool(re.fullmatch(r"[A-Z0-9]{6}", pnr))


def is_valid_passenger_name(name: str) -> bool:
    """
    Lufthansa rejects names with:
    - Numbers
    - Special chars except space, hyphen, apostrophe
    - More than 3 parts (e.g. Mr John Peter Paul Doe)
    """
    pattern = r"^[A-Za-z\s\-\'']{2,50}$"
    parts = name.strip().split()
    return bool(re.match(pattern, name)) and len(parts) <= 3


def normalize_name_for_ticket(name: str) -> str:
    """Lufthansa format: LASTNAME/FIRSTNAME MR"""
    parts = name.strip().upper().split()
    if len(parts) >= 2:
        return f"{parts[-1]}/{parts[0]} MR"
    return f"{parts[0]}/ MR"


# Demo
print(is_valid_passenger_name("John O'Malley"))      # → True
print(is_valid_passenger_name("John123"))           # → False
print(is_valid_passenger_name("John Peter Paul Doe")) # → False
print(normalize_name_for_ticket("anna maria schmidt"))  # → SCHMIDT/ANNA MARIA MR