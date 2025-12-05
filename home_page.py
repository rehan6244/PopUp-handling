# pages/home_page.py — now only 40 lines!
from components.search_form import SearchForm
from components.overlay_manager import OverlayManager
from utils.smart_locator import SmartLocator

class HomePage:
    def __init__(self, page):
        self.page = page
        self.search = SearchForm(page)
        self.overlay = OverlayManager(page)
        
        # Auto-dismiss overlays on every page load
        self.overlay.dismiss_all()

    def open(self):
        self.page.goto("https://www.lufthansa.com/us/en/flight-search")
        self.page.wait_for_load_state("networkidle")
        return self

    def search_flights(self, 
                       origin="New York", dest="Berlin",
                       dep_date="12/15/2025", ret_date=None,
                       origin_code="JFK", dest_code="BER",
                       one_way=False):
        return (self
                .open()
                .search.fill_origin(origin, origin_code)
                .search.fill_destination(dest, dest_code)
                .search.select_dates(dep_date, ret_date or dep_date if not one_way else None)
                .search.submit())