import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

DATA_FILE = Path(__file__).parent / "data" / "test_data.json"


@pytest.fixture(scope="session")
def test_data():
    with DATA_FILE.open() as f:
        return json.load(f)


@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
