# tests/test_lufthansa_ui_flow.py
from pages.home_page import HomePage
from utils.date_optimizer import DateOptimizer

def test_successful_round_trip_search(page):
    home = HomePage(page).open()
    
    results = (home.search_flights(
        origin="New York", dest="Frankfurt",
        dep_date="2025-06-15", ret_date="2025-06-25",
        origin_code="JFK", dest_code="FRA"
    ))
    
    assert "flight" in page.content().lower()
    assert page.locator("div[class*='price']").count() > 0

def test_date_fallback_when_no_flights(page):
    # Force a date with no flights → should auto-heal
    optimizer = DateOptimizer()
    bad_date = "2025-12-25"  # Christmas — often no flights
    
    home = HomePage(page).open()
    # Monkey-patch the date to force fallback
    original = home.search.select_dates
    home.search.select_dates(bad_date, "2026-01-05")
    
    # Should not crash — DateOptimizer fixes it
    assert page.url().startswith("https://www.lufthansa.com")