import pytest
import allure

from pages.CartPage import CartPage
from pages.LoginPage import LoginPage
from pages.ProductPage import ProductPage
def test_add_to_cart(pages, soft_assert):
    login_page, product_page, cart_page = pages

    login_page.open_login_swag_labs('standard_user', 'secret_sauce')
    with allure.step("Verify product and add to cart"):
        soft_assert.assert_true(
            product_page.click_on_product1(),
            "Backpack was not displayed"
        )

    with allure.step("Verify product in cart"):
        soft_assert.assert_true(
            cart_page.verify_product_In_cart_page(),
            "Backpack was not found in cart"
        )

    cart_page.click_on_remove_from_cart_button()
    product_page.MenuButton()
    product_page.Logout()
    soft_assert.assert_all()

