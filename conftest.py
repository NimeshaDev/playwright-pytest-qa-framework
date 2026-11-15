import json
import os
import platform
from pathlib import Path

import pytest
import requests

DATA_FILE = Path(__file__).parent / "data" / "test_data.json"


@pytest.fixture(scope="session")
def test_data():
    with DATA_FILE.open() as f:
        return json.load(f)


@pytest.fixture(scope="session")
def api_base_url(test_data):
    return test_data["api_base_url"]


@pytest.fixture(scope="session")
def api_session():
    with requests.Session() as session:
        session.headers.update({"Accept": "application/json"})
        yield session


@pytest.fixture
def browser_page(page):
    """Playwright page from pytest-playwright (browser chosen with --browser)."""
    return page


def pytest_metadata(metadata, config):
    """Show browser, Python and commit in the HTML report's Environment section."""
    metadata.pop("JAVA_HOME", None)
    metadata["Python"] = platform.python_version()
    browsers = config.getoption("browser", default=None)
    if browsers:
        metadata["Browser"] = ", ".join(browsers)
    sha = os.environ.get("GITHUB_SHA")
    if sha:
        metadata["Commit"] = sha[:7]
        run_url = "{}/{}/actions/runs/{}".format(
            os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
            os.environ.get("GITHUB_REPOSITORY", ""),
            os.environ.get("GITHUB_RUN_ID", ""),
        )
        metadata["CI run"] = run_url


def pytest_html_report_title(report):
    report.title = "Playwright + pytest QA Framework - Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the HTML report when a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    page = item.funcargs.get("page")
    html = item.config.pluginmanager.getplugin("html")
    if page is None or html is None:
        return
    try:
        png = page.screenshot(full_page=True, type="png")
    except Exception:
        return
    import base64
    extras = getattr(report, "extras", [])
    extras.append(html.extras.png(base64.b64encode(png).decode()))
    report.extras = extras
