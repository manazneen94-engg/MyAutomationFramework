from selenium.webdriver.support.ui import WebDriverWait

from appium.webdriver.common.appiumby import AppiumBy
from pages.BasePage import BasePage

class CartPage(BasePage):
    # Cart page locators
    PRODUCT_NAME1_IN_CART_PAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sauce Labs Backpack")')
    REMOVE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("REMOVE")')

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        self.wait = WebDriverWait(driver, timeout)

    # reusable methods
    def verify_product_In_cart_page(self):
        product1 = self.find_element(self.PRODUCT_NAME1_IN_CART_PAGE)
        return product1.is_displayed()

    def click_on_remove_from_cart_button(self):
        self.click_element(self.REMOVE_BUTTON)

