import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def login_as(page, user):
    login = LoginPage(page)
    login.goto()
    login.login(user["username"], user["password"])


@pytest.mark.smoke
@pytest.mark.parametrize(
    "user_key, should_log_in",
    [
        ("valid_user", True),
        ("invalid_user", False),
        ("locked_user", False),
    ],
    ids=["valid", "invalid", "locked"],
)
def test_login(browser_page, test_data, user_key, should_log_in):
    login_as(browser_page, test_data[user_key])

    assert ("inventory" in browser_page.url) == should_log_in


def test_add_to_cart(browser_page, test_data):
    login_as(browser_page, test_data["valid_user"])
    inventory = InventoryPage(browser_page)

    inventory.add_first_item_to_cart()

    assert inventory.get_cart_count() == "1", "Cart badge should show 1"


@pytest.mark.smoke
def test_complete_flow(browser_page, test_data):
    login_as(browser_page, test_data["valid_user"])
    inventory = InventoryPage(browser_page)
    cart = CartPage(browser_page)

    assert inventory.is_loaded(), "Inventory page not loaded"
    inventory.add_first_item_to_cart()
    assert inventory.get_cart_count() == "1"

    cart.goto()
    assert cart.is_loaded(), "Cart page not loaded"
    assert cart.get_item_count() == 1, "Cart should have 1 item"
