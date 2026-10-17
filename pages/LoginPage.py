

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from pages.BasePage import BasePage


class LoginPage(BasePage):

    #Locators for Swag Labs
    SWAG_USERNAME = (AppiumBy.XPATH,'//android.widget.EditText[@content-desc="test-Username"]')
    SWAG_PASSWORD = (AppiumBy.XPATH,'//android.widget.EditText[@content-desc="test-Password"]')
    SWAG_LOGIN_BUTTON = (AppiumBy.XPATH, '//android.widget.TextView[@text="LOGIN"]')
    SWAG_ERROR_MESSAGE_CRED = (AppiumBy.XPATH, '//android.widget.TextView[@text="Username and password do not match any user in this service."]')
    SWAG_ERROR_USERNAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Username is required")')
    SWAG_ERROR_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Password is required")')

    # Xpath for all invalid login error msgs
    SWAG_ERROR_MESSAGE = (
        AppiumBy.XPATH,
        '//android.widget.TextView['
        'contains(@text, "Invalid") or '
        'contains(@text, "required") or '
        'contains(@text, "do not match")]'
    )

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        self.wait = WebDriverWait(driver, timeout)

    #swag Labs reusable Methods:
    def open_login_swag_labs(self, username, password):
        self.enter_text(self.SWAG_USERNAME, username)
        self.enter_text(self.SWAG_PASSWORD, password)
        self.click_login_button(self.SWAG_LOGIN_BUTTON)

    def get_error_message(self):
        element = self.find_element(self.SWAG_ERROR_MESSAGE)
        return element.text

    def username_field(self, locator):
        element = self.find_element(locator)
        return element.text

    def password_field(self, locator):
        element = self.find_element(locator)
        return element.text

    def click_login_button(self,locator):
        self.click_element(self.SWAG_LOGIN_BUTTON)

    def is_login_button_displayed(self,locator):
        return self.is_buttonDisplayed(self.SWAG_LOGIN_BUTTON)

    def error_msg_cred(self,locator):
        element = self.find_element(self.SWAG_ERROR_MESSAGE_CRED)
        return element.text

    def error_username(self,locator):
        element = self.find_element(self.SWAG_ERROR_USERNAME)
        return element.text

    def error_password(self,locator):
        element = self.find_element(self.SWAG_ERROR_PASSWORD)
        return element.text






