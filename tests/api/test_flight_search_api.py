# tests/api/test_flight_search_api.py
import json
from datetime import datetime, timedelta

def test_real_lufthansa_search_api(api_client):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    in_two_weeks = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    params = {
        "origin": "FRA",
        "destination": "JFK",
        "departureDate": tomorrow,
        "returnDate": in_two_weeks,
        "cabinClass": "ECONOMY",
        "adults": 1,
        "client": "lufthansa.com"
    }
    
    # Real public endpoint used by lufthansa.com (no auth needed!)
    response = api_client.get(
        "https://www.lufthansa.com/api/flights/search",
        params=params,
        timeout=20
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Real contract validation
    assert "outbound" in data
    assert "return" in data
    assert len(data["outbound"]["flights"]) > 0
    assert data["outbound"]["flights"][0]["price"]["total"] > 0
    
    # Validate price breakdown matches total
    flight = data["outbound"]["flights"][0]
    expected = flight["price"]["base"] + flight["price"]["taxes"] + flight["price"].get("surcharges", 0)
    assert abs(expected - flight["price"]["total"]) < 0.02  # 1 cent tolerance