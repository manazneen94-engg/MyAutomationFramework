import allure

class SoftAssert:
    def __init__(self):
        self.errors = []

    def assert_true(self, condition, message="Condition failed"):
        if not condition:
            self.errors.append(message)
            allure.attach(
                message,
                name="SoftAssert Failure",
                attachment_type=allure.attachment_type.TEXT
            )

    def assert_equal(self, actual, expected, message="Values not equal"):
        if actual != expected:
            error_msg = f"{message} | Expected: {expected}, Actual: {actual}"
            self.errors.append(error_msg)
            allure.attach(
                error_msg,
                name="SoftAssert Failure",
                attachment_type=allure.attachment_type.TEXT
            )

    def assert_all(self):
        if self.errors:
            raise AssertionError("\n".join(self.errors))
