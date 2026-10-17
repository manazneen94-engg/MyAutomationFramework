from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



from appium.webdriver.common.appiumby import AppiumBy
from pages.BasePage import BasePage


class ProductPage(BasePage):

    # Product page locators
    PRODUCTS_TITLE = (AppiumBy.XPATH,'//android.widget.TextView[@text="PRODUCTS"]' )
    PRODUCT_NAME1 = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Sauce Labs Backpack")')
    ADD_TO_CART_BUTTON = (AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="test-ADD TO CART"]')
    CART_ICON = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.ImageView").instance(3)')

    # Menu locators
    MENU_BUTTON_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    LOGOUT_BUTTON_LOCATOR = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("test-LOGOUT")')

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        self.wait = WebDriverWait(driver, timeout)


    #reusable methods
    def verify_products_Title(self):
        return self.get_text(self.PRODUCTS_TITLE)

    def MenuButton(self):
        self.click_element(self.MENU_BUTTON_LOCATOR)

    def Logout(self):
        self.click_element(self.LOGOUT_BUTTON_LOCATOR)

    def click_on_product1(self):
        product = self.find_element(self.PRODUCT_NAME1)
        if product.is_displayed():
            self.click_element(self.ADD_TO_CART_BUTTON)
            self.click_element(self.CART_ICON)
            return True
        return False

