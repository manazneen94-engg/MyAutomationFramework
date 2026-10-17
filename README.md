# Swag Labs Mobile Automation Framework

A Python mobile test automation framework for the Swag Labs Android application, built with Appium, Pytest, and the Page Object Model (POM).

This README describes the framework for one Android device at a time. Parallel testing is intentionally excluded.

## Contents
- Project Overview
- Technology Stack
- Framework Folder Structure
- Prerequisites
- Setup
- Configuration
- Test Scenarios
- How to Run Tests
- Allure Reports
- Failure Evidence
- Framework Components
- Troubleshooting

---

## Project Overview
The framework automates common user journeys in the Swag Labs Android app:
- Log in with valid credentials and verify the Products page.
- Run invalid-login scenarios using data stored in an Excel spreadsheet.
- Add a product to the cart and verify that it appears in the cart.
- Remove a product from the cart.
- Log out and verify that the login screen is displayed.

Reusable page objects keep tests readable. Pytest fixtures manage the driver and shared test dependencies. Allure records test steps and can include screenshots, page source, and device logs when a test fails.

---

## Technology Stack
| Tool or library | Purpose |
|---|---|
| Python | Programming language |
| Appium | Mobile automation server |
| Appium-Python-Client | Python interface for Appium |
| UiAutomator2 | Android automation driver |
| Pytest | Test runner, fixtures, parametrization |
| Selenium support libraries | Explicit waits and expected conditions |
| openpyxl | Reading test data from Excel |
| Allure Pytest | Test steps, attachments, reporting |
| ADB | Android device connection and log collection |

---

## Framework Folder Structure
Keep the names aligned with files present in the repository. Example structure:

```
SwagLabs/
│
├── app/
│   └── SwagLabs.apk                 # Android application under test
│
├── pages/
│   ├── __init__.py
│   ├── BasePage.py                  # Shared waits and reusable UI actions
│   ├── LoginPage.py                 # Login screen locators and actions
│   ├── ProductPage.py               # Products, add-to-cart, menu, logout
│   └── CartPage.py                  # Cart item checks and remove action
│
├── tests/
│   ├── test_LoginFlow.py            # Valid, invalid, and logout scenarios
│   └── test_AddToCart.py            # Add-to-cart and cart verification
│
├── testData/
│   └── InValidUsers.xlsx            # Invalid-login test data
│
├── utils/
│   ├── __init__.py
│   ├── Excel_Reader.py              # Loads rows from Excel
│   ├── soft_assert.py               # Collects soft assertion failures
│   └── appium_server.py             # Starts/stops the Appium server
│
├── reports/
│   ├── screenshots/                 # Failure screenshots (generated)
│   ├── logs/                        # Device logs (generated)
│   └── page_source/                 # XML page source (generated)
│
├── allure-results/                  # Raw Allure results (generated)
├── conftest.py                      # Driver and shared Pytest fixtures/hooks
├── pytest.ini                        # Pytest discovery/default options
├── requirements.txt                  # Python dependencies
├── .gitignore
└── README.md
```

### What each main folder is for
- `app/` — stores the APK used for testing.
- `pages/` — contains page classes and locators. UI operations belong here rather than being duplicated in test methods.
- `tests/` — contains test cases and assertions for user journeys.
- `testData/` — stores external test inputs such as invalid usernames, passwords, and expected error messages.
- `utils/` — contains reusable helpers, including Excel reading, soft assertions, and Appium server management.
- `reports/` and `allure-results/` — hold generated evidence and reporting files (not source code).
- `conftest.py` — provides fixtures shared by tests, including the Appium driver, page objects, soft assertion object, and failure-artifact hook.

---

## Prerequisites
Install and configure:
- Python and pip
- Node.js and npm
- Appium server
- Appium UiAutomator2 driver
- Android SDK Platform Tools (`adb`)
- An Android phone with Developer options and USB debugging enabled
- Swag Labs APK (included in `apps/`)
- Allure command-line tool (optional, for opening reports)

Check your Python installation:
```powershell
py --version
```

Check that your phone is connected and authorized:
```powershell
adb devices -l
```
Your phone should show status `device`. If `unauthorized`, unlock the phone and approve the USB debugging prompt.

Check Appium and installed drivers:
```powershell
appium --version
appium driver list --installed
```

Install UiAutomator2 if not installed:
```powershell
appium driver install uiautomator2
```

---

## Setup
1. Open the project directory

```powershell
cd C:\path\to\SwagLabs
```

Run commands from this directory so Pytest can find `pytest.ini`, `conftest.py`, the `tests` folder, and test data.

2. Create a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the environment interpreter directly:
```powershell
.\.venv\Scripts\python.exe --version
```

3. Install Python dependencies
Create or update `requirements.txt` and install:

```powershell
py -m pip install -r requirements.txt
```

4. Install the APK (if required)

```powershell
adb install -r app\SwagLabs.apk
```

The framework uses the package `com.swaglabsmobileapp` and activity `com.swaglabsmobileapp.MainActivity`. Verify these values if a different APK is used.

5. Start the Appium server
The `appium_server.py` helper can manage Appium lifecycle (via the `appium_server` fixture). To start Appium manually:

```powershell
appium --address 127.0.0.1 --port 4723
```

Do not run two Appium servers on the same port. The driver URL in `conftest.py` should match the server (e.g. `http://127.0.0.1:4723`).

---

## Configuration
The `driver` fixture in `conftest.py` must identify the Android device. Find device UDID:
```powershell
adb devices -l
```

Update capabilities in `conftest.py` accordingly, for example:
```python
options.platform_name = "Android"
options.device_name = "OnePlus"
options.automation_name = "UiAutomator2"
options.udid = "YOUR_ANDROID_DEVICE_UDID"
options.app_package = "com.swaglabsmobileapp"
options.app_activity = "com.swaglabsmobileapp.MainActivity"
options.no_reset = True
```
Replace `YOUR_ANDROID_DEVICE_UDID` with the actual UDID. Use `no_reset` based on your test isolation needs.

---

## Test Scenarios
**Login — `tests/test_LoginFlow.py`**
- Valid credentials navigate to Products page.
- Invalid credentials display expected validation message.
- Locked-out user receives appropriate error.
- Logging out returns user to login screen.

**Add to Cart — `tests/test_AddToCart.py`**
- Login with valid credentials.
- Add a product from Products page.
- Open cart and verify the product displays.
- Optionally remove product and logout as cleanup.

### Excel test data
`testData/InValidUsers.xlsx` should contain columns such as: `Username`, `Password`, `ExpectedResult`. Match column headings with keys used by `Excel_Reader.py`.

---

## How to Run Tests
Run all tests from project root:
```powershell
py -m pytest
```

Run login tests only:
```powershell
py -m pytest tests/test_LoginFlow.py -v -s
```

Run add-to-cart tests only:
```powershell
py -m pytest tests/test_AddToCart.py -v -s
```

Run a single test function:
```powershell
py -m pytest tests/test_AddToCart.py::test_add_to_cart -v -s
```

List discovered tests without running:
```powershell
py -m pytest --collect-only -q
```

---

## Pytest Configuration
Example `pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = -v -s --alluredir=allure-results
```
This writes raw Allure results to `allure-results` and configures discovery. Parallel testing is intentionally excluded.

---

## Allure Reports
Generate Allure results during test runs:
```powershell
py -m pytest
```
Open the report:
```powershell
allure serve allure-results
```
Clear `allure-results` before a fresh run to avoid mixing old and new results. Use `with allure.step("..."):` for named steps and `allure.attach(...)` to include files.

---

## Failure Evidence
`pytest_runtest_makereport` in `conftest.py` captures:
- Screenshot: `reports/screenshots/`
- Page source: `reports/page_source/`
- Android logcat: `reports/logs/`

Attach logs to Allure and inspect locally with `adb -s YOUR_ANDROID_DEVICE_UDID logcat -d`.

---

## Framework Components
**BasePage.py** — shared actions and explicit-wait helpers (click, type, scroll).

**Page classes**
- `LoginPage.py` — login actions, error message locators
- `ProductPage.py` — product listing, add-to-cart, menu, logout
- `CartPage.py` — cart checks and removal

Each page receives the driver in `__init__` and uses BasePage for common operations. Keep locators in page classes; keep assertions in tests.

**conftest.py** — manages Appium server lifecycle (optional), function-scoped driver, `pages` fixture (LoginPage, ProductPage, CartPage), `soft_assert` fixture, and failure artifact hook.

**soft_assert.py** — accumulates assertion failures; call `soft_assert.assert_all()` at test end.

**Excel_Reader.py** — loads rows for parameterized invalid-login tests. Keep Excel column names consistent.

---

## Troubleshooting
- `pytest` not recognized: run via Python: `py -m pytest` and ensure virtual env is activated.
- Appium connection refused: ensure Appium is running at `127.0.0.1:4723` and the driver URL matches.
- Android device not detected: `adb devices -l` — reconnect or enable USB debugging.
- `NoSuchElementException` / `TimeoutException`: verify app screen, inspect page source, prefer resource/accessibility IDs, use explicit waits.
- Invalid-login assertion mismatch: print `expected`/`actual` with `!r` to reveal whitespace. Confirm Excel values match the app version.
- Driver not closed: ensure `driver.quit()` is called in fixture `finally` block.

---
