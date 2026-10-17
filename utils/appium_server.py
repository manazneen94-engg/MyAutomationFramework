from appium.webdriver.appium_service import AppiumService


appium_service = AppiumService()


def start_appium_server():
    if not appium_service.is_running:
        appium_service.start(
            args=["--address", "127.0.0.1", "-p", "4723"]
        )

    print("Appium server started")


def stop_appium_server():
    if appium_service.is_running:
        appium_service.stop()
        print("Appium server stopped")