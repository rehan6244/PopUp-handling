tests/
├── conftest.py                  ← shared fixtures (browser, storage_state, etc.)
├── test_baggage_rules.py
├── test_fare_rules.py
├── test_price_consistency.py
├── test_pnr_validation.py
└── test_lufthansa_ui_flow.py    ← real UI test using your self-healing POM



tests/
└── api/
    ├── conftest.py                 ← shared API client + auth
    ├── test_flight_search_api.py   ← Real Lufthansa/SWISS public API
    ├── test_booking_api.py         ← Mocked booking flow (real contracts)
    ├── test_price_consistency_api.py
    └── fixtures/
        └── sample_search_response.json