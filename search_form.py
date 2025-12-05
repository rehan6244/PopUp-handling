# components/search_form.py
from utils.smart_locator import SmartLocator
from typing import Optional
from datetime import datetime

class SearchForm:
    def __init__(self, page):
        self.page = page

        # Smart, self-healing locators with fallbacks
        self.origin = SmartLocator(page, [
            "input[name*='originCode']",
            "input[placeholder*='From']",
            "input[aria-label*='origin']",
            "text=From >> .. >> input",
        ], "Origin field")

        self.destination = SmartLocator(page, [
            "input[name*='destinationCode']",
            "input[placeholder*='To']",
            "input[aria-label*='destination']",
            "text=To >> .. >> input",
        ], "Destination field")

        self.departure_date = SmartLocator(page, [
            "input[name*='travelDatetime']:nth-child(1)",
            "input[placeholder*='Departure']",
        ], "Departure date input")

        self.search_button = SmartLocator(page, [
            "button:has-text('Search flights')",
            "button:has-text('Show flights')",
            "button[type='submit'] >> visible=true",
            "[data-testid*='search'] button",
        ], "Search button")

    def fill_origin(self, city: str, code: Optional[str] = None) -> 'SearchForm':
        self.origin.fill(city, delay=100)
        self.page.wait_for_timeout(1500)
        if code:
            self.page.locator(f"div[role='option']:has-text('{code}')").first.click(timeout=5000)
        else:
            self.page.keyboard.press("Enter")
        return self

    def fill_destination(self, city: str, code: Optional[str] = None) -> 'SearchForm':
        self.destination.fill(city, delay=100)
        self.page.wait_for_timeout(1500)
        if code:
            self.page.locator(f"div[role='option']:has-text('{code}')").first.click(timeout=5000)
        else:
            self.page.keyboard.press("Enter")
        return self

    def select_dates(self, dep: str, ret: Optional[str] = None) -> 'SearchForm':
        # Try normal calendar → fallback to JS injection → fallback to ML date optimizer
        try:
            self.departure_date.click()
            self.page.wait_for_selector("div[class*='calendar']", timeout=8000)
            self._select_via_calendar(dep)
            if ret:
                self._select_via_calendar(ret)
        except:
            # Your existing ML DateOptimizer fallback here
            from utils.date_optimizer import DateOptimizer
            dep = DateOptimizer().suggest_valid_date(dep)
            if ret:
                ret = DateOptimizer().suggest_valid_date(ret)
            self._inject_dates_js(dep, ret)
        return self

    def _select_via_calendar(self, date_str: str):
        month, day, year = date_str.split('/')
        month_name = datetime.strptime(month, "%m").strftime("%B")
        day = str(int(day))

        # Navigate month
        while month_name not in self.page.locator("div[class*='calendar'] h2, span[class*='month']").first.text_content():
            self.page.click("button[aria-label*='Next']", timeout=3000)

        # Click day with multiple strategies
        self.page.click(f"button:has-text('{day}') >> visible=true", timeout=5000)

    def _inject_dates_js(self, dep: str, ret: Optional[str]):
        self.page.evaluate(f"""
            () => {{
                const inputs = document.querySelectorAll('input[name*="travelDatetime"]');
                inputs[0].value = '{dep}'; inputs[0].dispatchEvent(new Event('change', {{bubbles:true}}));
                {f"inputs[1].value = '{ret}'; inputs[1].dispatchEvent(new Event('change', {{bubbles:true}}));" if ret else ""}
            }}
        """)

    def submit(self):
        self.search_button.click()
        from pages.results_page import ResultsPage
        return ResultsPage(self.page)