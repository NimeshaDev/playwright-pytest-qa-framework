class CartPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.saucedemo.com/cart.html"

    def goto(self):
        self.page.locator(".shopping_cart_link").click()
        self.page.wait_for_url("**/cart.html")

    def is_loaded(self):
        return "cart" in self.page.url

    def get_item_count(self):
        self.page.locator(".cart_list").wait_for()
        return self.page.locator(".cart_item").count()
