# MyAutomationFramework — Mobile UI Automation (Appium)

Purpose
I implemented a mobile UI automation framework (Android) using Appium to demonstrate stable, maintainable end-to-end tests for common user flows (login, negative login, logout, plus one additional flow). This repo is submitted as part of my Wipro technical assessment.

Summary of what this submission contains
- A framework implemented by me that follows Page Object Model (POM), central driver management, data-driven test examples, and failure handling (screenshots, logs, reports).
- Example Android APK reference (place your APK in the repository as described below).
- Clear commands to run tests locally and in CI, and notes on how I used AI and how I handle flaky tests and other issues.

Table of contents
- Prerequisites
- Files & recommended layout
- Configure the project
- Quick commands (install APK, start Appium, run tests)
- How tests are executed (runtime flow)
- Design decisions and key components
- Flakiness handling and troubleshooting
- How I used AI (explicit)
- What is included / what is not covered
- Sample reports / artifacts
- Contact & license

Prerequisites (local machine)
- JDK 11 or 17
  - verify: java -version
- Maven (if using Maven build)
  - verify: mvn -v
- Node.js + Appium server
  - Install Appium: npm install -g appium
  - or run with npx: npx appium
- Android SDK (for Android)
  - Set ANDROID_HOME and PATH to include platform-tools and tools/bin
  - Create an AVD using avdmanager / android emulator, or use a connected device
- Xcode + simulator (for iOS; macOS only)
- (Optional) Allure commandline for reports:
  - brew install allure or follow instructions at docs

Quick start (Android / Java + Maven example)

1. Start Appium
   - npx appium
   - or appium &   (runs in background)

2. Start emulator (Android example)
   - $ANDROID_HOME/emulator/emulator -avd <AVD_NAME>

3. Run full test suite
   - mvn clean test

4. Run a specific test class
   - mvn -Dtest=com.mycompany.tests.MyLoginTest test

5. Run tests with a Maven profile (example profiles: android-emulator, android-device, ios-simulator)
   - mvn clean test -Pandroid-emulator

6. Generate and open Allure report (if configured)
   - mvn test
   - mvn allure:serve   # this will run a temporary server and open the report

APK in this repo (prerequisite)
- Place the Android APK you want to test under:
  - apps/android/MyApp-debug.apk
- If you already included an APK, ensure the path above matches. If not present, add the APK before running tests.

Recommended file layout (actual implementation may use these paths)
.
├─ apps/                        # put your APK(s) here (apps/android/*.apk)
├─ configs/                     # environment properties / capability profiles
│  └─ default.properties
├─ drivers/                     # driver utilities or helper scripts
├─ src/
│  ├─ main/
│  │  ├─ java/
│  │  │  ├─ com/mycompany/framework/
│  │  │  │  ├─ driver/         # DriverFactory, SessionManager
│  │  │  │  ├─ utils/          # helpers: log, wait, screenshot
│  │  │  │  └─ config/         # capability builders, config readers
│  ├─ test/
│  │  ├─ java/
│  │  │  ├─ com/mycompany/tests/
│  │  │  │  ├─ pages/          # Page objects / screen objects
│  │  │  │  ├─ tests/          # TestNG or JUnit test classes
│  │  │  │  └─ data/           # test data providers / fixtures
├─ reports/                 # generated reports, screenshots, logs
├─ scripts/                 # helper scripts (start-emulator.sh, install-apk.sh)
├─ pom.xml                  # Maven build (if Java)
└─ README.md

Configuration approach
- Config files (preferred): configs/default.properties, configs/android-emulator.properties, configs/android-device.properties
- Environment variables (optional override):
  - APPIUM_SERVER — e.g. http://localhost:4723/wd/hub
  - PLATFORM_NAME — Android
  - APP_PATH — path to APK (defaults to apps/android/MyApp-debug.apk)
  - DEVICE_NAME / UDID / PLATFORM_VERSION
- The framework reads configs first, then allows overrides via system properties or environment variables for CI flexibility:
  - Example Maven override: mvn test -Dapp.path=/tmp/app.apk -Ddevice.name=Pixel_3

Example config (configs/default.properties)
appium.server=http://localhost:4723/wd/hub
platform.name=Android
device.name=Pixel_3_API_30
platform.version=11.0
app.path=apps/android/MyApp-debug.apk
automation.name=UiAutomator2

Start Appium in a known state
- If you use uiAutomator2 and adb:
  adb devices
  adb -s <deviceId> install path/to/app.apk

Running on iOS (macOS only)
- Ensure Xcode, Carthage/CocoaPods if needed, and proper signing config are present.
- Use platformName=iOS and appropriate deviceName (Simulator) or udid for real device.

Running with Docker (optional)
- You can run Appium server in Docker. Example:
  docker run -d -p 4723:4723 --name appium appium/appium

CI (example notes)
- Example CI steps:
  - Setup JDK, Node and Appium (or start Appium service)
  - Start emulator (Android) or use device farm (BrowserStack / Sauce Labs)
  - Run mvn -DskipTests=false test
  - Publish reports/ and screenshots/ as build artifacts
- Save the reports/ directory and Allure results for analysis.

How tests execute (brief)
- Tests call methods in page/screen objects.
- Page objects use the DriverFactory to access an AppiumDriver.
- DriverFactory reads a config profile (e.g., android-emulator, android-device, ios-simulator).
- Tests are data-driven where needed via TestNG data providers or CSV/JSON fixtures.
- On failure, the framework captures a screenshot and stores logs under reports/.

Design decisions and key components (what I implemented and why)
- Page Object Model: each screen/page is a dedicated class with clear actions and element locators.
- DriverFactory: centralizes AppiumDriver creation and applies capability profiles.
- Config separation: environment-specific settings are stored in configs/ and not hard-coded.
- Retry & stability: implemented a retry analyzer (TestNG) for transient failures and explicit wait utilities to reduce flakiness.
- Screenshots & logs: on-failure hooks capture screenshots and save driver logs to reports/.
- Data-driven tests: data providers read CSV/JSON to run the same test with multiple data sets.
- Parallel runs: ThreadLocal driver handling allows running tests in parallel without session collision.
- Extensibility: adding a new device profile or page object is straightforward — follow the folder pattern.

Flakiness handling and reliability measures (concrete)
- Locators: use resource-id / accessibility-id where possible to avoid brittle XPath.
- Synchronization: explicit waits and utility wait methods to reduce flakiness.
- Retry Analyzer: re-run flaky tests a configurable small number of times (TestNG retry analyzer) while logging retries.
- Test isolation: each test starts from a known app state (clear app data or restart app as required).
- Timeouts: conservative timeouts for operations and a configurable newCommandTimeout to avoid session drop.
- Backoff & health checks: before test run, verify Appium server and device are reachable (adb devices, Appium health endpoint).
- Artifacts for debugging: on failure save screenshot, page source, and device logs (adb logcat) to reports/.
- CI strategy: run smoke subset on every push; schedule full/regression runs off-peak or on device farm to reduce flakiness due to emulator startup times.

How I used AI (explicit statement for the assessment)
I used AI tools during design and development for non-proprietary tasks:
- Research & comparison: validate options (Appium client versions, TestNG vs JUnit, Allure config) and get example capability snippets.
- Design assistance: generate README drafts, sample config files, and example DriverFactory / retry-analyzer pseudocode to speed iteration.
- Troubleshooting guidance: quick suggestions for common Appium errors (e.g., session creation issues, platform capability mismatches) — I validated fixes myself.
- Code templates: generate small helper templates (e.g., wait utilities, screenshot helper) which I reviewed and adapted to fit the final implementation.
Note: I did not copy any proprietary code; everything generated or referenced was checked and adapted by me.

What is included in this submission
- Framework source (POM, DriverFactory, Page Objects, tests) — if you see only README now, the code will be available in the repository. (If the code is missing, please check the repo branch or I can push it on request.)
- APK placement instruction and sample config to run tests against the APK you include.
- Failure handling, screenshots, and reporting configuration.

What is NOT covered in this repo (intentionally)
- Full cross-platform implementation for iOS (iOS notes and capability guidance are present but iOS tests are not included).
- BDD (Cucumber/SpecFlow) style implementation — not implemented in submitted code.
- Tagging (smoke/regression tagging using a runner’s tag system) — not implemented in submitted code.
- API tests — not part of this submission.

Sample report / artifacts
- After a test run, artifacts are located under:
  reports/
  ├─ screenshots/
  ├─ logs/
  └─ allure-results/   (if Allure is enabled)
- Example: reports/screenshots/LoginTest_shouldLogin_success_2026-10-17-12-00-00.png

Troubleshooting tips (common failures)
- Appium server not reachable:
  - Check APPIUM_SERVER config and run npx appium; verify port 4723 is open.
- Device not found:
  - Run adb devices and ensure emulator/device is online.
- APK install fails:
  - adb uninstall <pkg> && adb install -r apps/android/MyApp-debug.apk
- Flaky element not found:
  - replace brittle locator, add explicit wait, or retry the action with a small backoff.

Notes for reviewers (how to evaluate)
- Check src/test/java/.../pages for page object separation.
- Check DriverFactory (or equivalent) for capability handling.
- Run mvn -Dtest=... to run specific tests and see reports in reports/.
- Inspect retry and wait utilities to evaluate stability considerations.

Contact
- Repository owner: manazneen94-engg
- For questions during the technical round: open an issue in this repo or message me directly.

License
- See LICENSE in this repo.
