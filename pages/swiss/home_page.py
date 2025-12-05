# pages/swiss/home_page.py
from pages.shared.base_page import BasePage
from pages.swiss.components.search_form import SwissSearchForm
from pages.swiss.components.overlay_manager import SwissOverlayManager

class SwissHomePage(BasePage):
    URL = "https://www.swiss.com/ch/en/homepage"

    def __init__(self, page):
        super().__init__(page)
        self.search = SwissSearchForm(page)
        self.overlay = SwissOverlayManager(page)
        self.overlay.dismiss_all()  # auto-run

    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")
        return self

    def search_flights(
        self,
        origin="Zurich", dest="New York",
        dep_date="2025-06-15", ret_date="2025-06-25",
        origin_code="ZRH", dest_code="JFK",
        one_way=False
    ):
        return (self
                .open()
                .search.fill_origin(origin, origin_code)
                .search.fill_destination(dest, dest_code)
                .search.select_dates(dep_date, ret_date if not one_way else None)
                .search.submit())