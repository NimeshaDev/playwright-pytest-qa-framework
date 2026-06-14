import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def logged_in_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        yield page
        browser.close()


def test_products_page_loads(logged_in_page):
    assert logged_in_page.url == "https://www.saucedemo.com/inventory.html"

def test_product_count(logged_in_page):
    items = logged_in_page.locator(".inventory_item")
    assert items.count() == 6