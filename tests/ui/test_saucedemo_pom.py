from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def login_as(page, user):
    login = LoginPage(page)
    login.goto()
    login.login(user["username"], user["password"])


def test_valid_login(browser_page, test_data):
    login_as(browser_page, test_data["valid_user"])
    assert "inventory" in browser_page.url, "Valid user should reach the inventory page"


def test_invalid_login(browser_page, test_data):
    login_as(browser_page, test_data["invalid_user"])
    assert "inventory" not in browser_page.url, "Invalid user should not log in"


def test_locked_user_login(browser_page, test_data):
    login_as(browser_page, test_data["locked_user"])
    assert "inventory" not in browser_page.url, "Locked user should not log in"


def test_add_to_cart(browser_page, test_data):
    login_as(browser_page, test_data["valid_user"])
    inventory = InventoryPage(browser_page)
    inventory.add_first_item_to_cart()
    assert inventory.get_cart_count() == "1", "Cart badge should show 1"


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
