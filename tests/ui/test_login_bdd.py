import pytest
from pytest_bdd import given, scenarios, then, when

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui

scenarios("login.feature")


@pytest.fixture
def context(browser_page, test_data):
    return {
        "page": browser_page,
        "login": LoginPage(browser_page),
        "inventory": InventoryPage(browser_page),
        "data": test_data,
    }


def _login(context, user_key):
    user = context["data"][user_key]
    context["login"].login(user["username"], user["password"])


@given("I am on the login page")
def go_to_login(context):
    context["login"].goto()


@when("I login with valid credentials")
def login_valid(context):
    _login(context, "valid_user")


@when("I login with invalid credentials")
def login_invalid(context):
    _login(context, "invalid_user")


@when("I login with locked user credentials")
def login_locked(context):
    _login(context, "locked_user")


@then("I should see the inventory page")
def check_inventory(context):
    assert "inventory" in context["page"].url, "Login failed"


@then("I should not see the inventory page")
def check_not_inventory(context):
    assert "inventory" not in context["page"].url, "User should not be logged in"
