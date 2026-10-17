import pytest
import subprocess
import allure

import os
from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.soft_assert import SoftAssert

from pages.LoginPage import LoginPage
from pages.ProductPage import ProductPage
from pages.CartPage import CartPage



from utils.appium_server import (
    start_appium_server,
    stop_appium_server
)


@pytest.fixture(scope="session", autouse=True)
def appium_server():
    start_appium_server()

    yield

    stop_appium_server()



@pytest.fixture(scope="function")
def driver(appium_server):

    print("Creating Appium driver...", flush=True)

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "OnePlus"
    options.automation_name = "UiAutomator2"
    options.udid = "KFGQOFGA55SGVWXO"

    options.app_package = "com.swaglabsmobileapp"
    options.app_activity = "com.swaglabsmobileapp.MainActivity"
    options.app_wait_duration = 30000
    options.no_reset = True

    driver = None

    try:
        driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=options
        )

        print("Appium driver created successfully.", flush=True)

        package = "com.swaglabsmobileapp"

        if not driver.is_app_installed(package):
            raise RuntimeError(
                f"Swag Labs app is not installed: {package}"
            )

        # Launch or bring the app to the foreground
        driver.activate_app(package)

        # Wait for the app UI to load
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import TimeoutException

        wait = WebDriverWait(driver, 20)

        try:
            wait.until(
                lambda d: d.current_package == package
            )
        except TimeoutException:
            print(
                "Expected app package not in foreground.",
                flush=True
            )

        print("Current package:", driver.current_package)
        print("Current activity:", driver.current_activity)

        print("Page source after app launch:")
        print(driver.page_source)

        driver.implicitly_wait(10)

        yield driver

    finally:
        if driver is not None:
            print("Closing driver...", flush=True)
            driver.quit()

@pytest.fixture
def pages(driver):
    return (
        LoginPage(driver),
        ProductPage(driver),
        CartPage(driver)
    )

@pytest.fixture
def soft_assert():
    return SoftAssert()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # Only capture artifacts when the actual test fails
    if report.when != "call" or not report.failed:
        return

    # Get Appium driver from fixture
    driver = item.funcargs.get("driver")

    if driver is None:
        print("Driver not available.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # -------------------------------------------------
    # Create directories
    # -------------------------------------------------

    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/logs", exist_ok=True)
    os.makedirs("reports/page_source", exist_ok=True)

    # =================================================
    # Screenshot
    # =================================================
    device_name = driver.capabilities.get("deviceName", "unknown_device")

    screenshot_path = (
        f"reports/screenshots/"
        f"{device_name}_{item.name}_{timestamp}.png"
    )

    driver.save_screenshot(screenshot_path)

    # Attach screenshot to Allure
    allure.attach.file(
        screenshot_path,
        name=f"{item.name}_screenshot",
        attachment_type=allure.attachment_type.PNG
    )

    # =================================================
    # Page source
    # =================================================

    page_source_path = (
        f"reports/page_source/"
        f"{item.name}_{timestamp}.xml"
    )

    with open(
        page_source_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(driver.page_source)

    # Attach page source to Allure
    allure.attach.file(
        page_source_path,
        name=f"{item.name}_page_source",
        attachment_type=allure.attachment_type.XML
    )

    # =================================================
    # Android logcat
    # =================================================

    log_path = (
        f"reports/logs/"
        f"{item.name}_{timestamp}.log"
    )

    result = subprocess.run(
        ["adb", "logcat", "-d"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    with open(
        log_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(result.stdout)

    # Attach logcat to Allure
    allure.attach.file(
        log_path,
        name=f"{item.name}_logcat",
        attachment_type=allure.attachment_type.TEXT
    )

    # -------------------------------------------------
    # Console output
    # -------------------------------------------------

    print("\n========== FAILURE ARTIFACTS ==========")
    print(f"Screenshot : {screenshot_path}")
    print(f"Page source: {page_source_path}")
    print(f"Logcat     : {log_path}")
    print("=======================================")