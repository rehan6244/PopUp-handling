# pages/base_page.py
from playwright.sync_api import Page, Locator
from utils.smart_locator import SmartLocator
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """Shared base for ALL Lufthansa Group brands (LH, LX, OS, EN, etc.)"""
    
    URL = ""  # Must be overridden in child
    
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str = None):
        url = url or self.URL
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=30000)

    def wait_for_selector(self, selector: str, **kwargs):
        return self.page.wait_for_selector(selector, **kwargs)

    def wait_for_timeout(self, ms: int):
        self.page.wait_for_timeout(ms)

    def get_element(self, selectors: list | str) -> Locator:
        """Wrapper that uses SmartLocator automatically"""
        if isinstance(selectors, str):
            selectors = [selectors]
        return SmartLocator(self.page, selectors, ",".join(selectors))._first_visible()
        
    def get_elements(self, selectors: list | str):
        if isinstance(selectors, str):
            selectors = [selectors]
        return self.page.locator(selectors[0])  # fallback to first