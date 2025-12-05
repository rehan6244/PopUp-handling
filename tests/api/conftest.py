# tests/api/conftest.py
import pytest
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    
    # Real Lufthansa/SWISS public search endpoint (2025)
    session.base_url = "https://api.lufthansa.com/v1"
    
    # Real headers from browser (copy from devtools → Network → any XHR)
    session.headers.update({
        "Accept": "application/json",
        "Origin": "https://www.lufthansa.com",
        "Referer": "https://www.lufthansa.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    
    # Retry logic — Lufthansa API flakes sometimes
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    
    return session