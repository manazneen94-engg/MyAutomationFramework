
import pytest
import allure

from pages.LoginPage import LoginPage
from pages.ProductPage import ProductPage

from utils.Excel_Reader import get_excel_data


INVALID_LOGIN_DATA = get_excel_data("Sheet1")


def get_user_data():
    return [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce")
    ]

#Simple one round of Login and Logout scenario and verify if Login Page is displayed.
@pytest.mark.smoke
@pytest.mark.order(1)
def test_Login_Logout(pages, soft_assert, username, password):
    login_page, product_page, cart_page = pages

    login_page.open_login_swag_labs('standard_user', 'secret_sauce')
    product_page.MenuButton()
    product_page.Logout()

    # verifying if Login button displayed after the logout
    with allure.step("Verify login button is displayed after logout"):
        soft_assert.assert_true(
            login_page.is_login_button_displayed(login_page.SWAG_LOGIN_BUTTON),
            "Login button not displayed after logout"
        )
    soft_assert.assert_all()


#Login & Verify Products Title and Logut from app
@pytest.mark.smoke
@pytest.mark.order(2)
@pytest.mark.parametrize("username,password", get_user_data())
def test_Login_Verify_Title(pages, soft_assert, username, password):
    login_page, product_page, cart_page = pages

    login_page.open_login_swag_labs(username, password)

    actual_products_title = product_page.verify_products_Title()
    expected_products_title = "PRODUCTS"

    #verifying here, if PRODUCTS title is displayed or not
    with allure.step("Verify Products Title is displayed in Products Page"):
        soft_assert.assert_equal(actual_products_title, expected_products_title, "Products page title mismatch")

    product_page.MenuButton()
    product_page.Logout()
    soft_assert.assert_all()

@pytest.mark.regression
@pytest.mark.order(3)
@pytest.mark.parametrize(
    "test_data",
    INVALID_LOGIN_DATA,
    ids=[
        f"row_{index + 2}"
        for index in range(len(INVALID_LOGIN_DATA))
    ]
)
def test_invalid_login_scenarios(pages, test_data, soft_assert):
    login_page, product_page, cart_page = pages

    username = test_data["Username"]
    password = test_data["Password"]
    expected_result = test_data["ExpectedResult"]

    # Enter username & password and click on Login.
    login_page.open_login_swag_labs(username, password)

    # Read the actual error displayed by the application.
    actual_result = login_page.get_error_message()

    # Validate actual result against Excel test data.
    assert actual_result == expected_result, (
        f"Login validation failed!\n"
        f"Username: {username!r}\n"
        f"Password: {password!r}\n"
        f"Expected: {expected_result!r}\n"
        f"Actual: {actual_result!r}"
    )
