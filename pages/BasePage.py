from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # find element
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    # find elements
    def find_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    # is_Displayed
    def is_buttonDisplayed(self, locator):
        try: return self.find_element(locator).is_displayed()
        except Exception:
            return False

    # click element
    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # enter text in element
    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    #getText
    def get_text(self, locator):
        element = self.driver.find_element(*locator).text
        return element

    # scroll till the element using text
    def scroll_to_element(self, text):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )

    # scroll till the element using resourceID
    def scroll_to_element_by_id(self, resource_id):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().resourceId("{resource_id}"))'
        )

    # Scroll using Content Description
    def scroll_to_element_by_description(self, description):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{description}"))'
        )

    # Scroll using Class Name
    def scroll_to_element_by_class(self, class_name):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().className("{class_name}"))'
        )

    # Scroll using an instance index - Use this when the target is identified by its position among elements of the same type
    def scroll_to_element_by_instance(self, class_name, index):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().className("{class_name}")'
            f'.instance({index}))'
        )

    #   swipe
    def swipe(self, direction, duration=500):

        size = self.driver.get_window_size()

        width = size["width"]
        height = size["height"]

        start_x = width // 2
        start_y = height // 2

        if direction == "up":
            start_y = int(height * 0.80)
            end_y = int(height * 0.20)
            end_x = start_x

        elif direction == "down":
            start_y = int(height * 0.20)
            end_y = int(height * 0.80)
            end_x = start_x

        elif direction == "left":
            start_x = int(width * 0.80)
            end_x = int(width * 0.20)
            end_y = start_y

        elif direction == "right":
            start_x = int(width * 0.20)
            end_x = int(width * 0.80)
            end_y = start_y

        else:
            raise ValueError(
                "Invalid direction. Use up, down, left, or right."
            )

        self.driver.swipe(
            start_x, start_y,
            end_x, end_y,
            duration
        )

    def start_App_Activity(self, app_package, app_activity):
        self.driver.start_activity(app_package, app_activity)