# Test Automation – Todo Mobile App

Automated UI tests for the **Todo** task-management mobile app (Android, with optional iOS support). Built with **Appium**, **Python**, **pytest**, and **Selene**.

## What’s in this project

- **Appium** – mobile automation
- **Selene** – fluent browser/element API and built-in waiting
- **pytest** – test runner and fixtures
- **Platform and device parametrization** – run with `--platform android` or `--platform ios`, and optionally `--device <id>` or `--device any` to pick the first connected device
- **CI** – GitHub Actions workflow runs tests on an Android emulator; device and platform come from `ci/config.yaml` or manual inputs

## Prerequisites

- **Python** 3.11+ (or 3.10)
- **Node.js** (for Appium)
- **Appium** 2.x with UIAutomator2 driver (Android)
- **Android**: device or emulator with the Todo app **installed**, or an APK path for (re)install (APK must be placed inside **ci** folder in order to install)
- **Appium server** running (e.g. `appium` on `http://127.0.0.1:4723`) when running tests locally

## Project structure

```
.
├── config.py                 # App/device config (env-based; used by tests and CI)
├── requirements.txt          # Python dependencies
├── app_test_plan.md          # Detailed test plan and scenarios
├── ci/
│   ├── config.yaml          # CI: platform & device (any_active or specific id)
│   └── README.md            # CI config and APK instructions
├── .github/workflows/
│   └── android-tests.yml    # Run tests on Android emulator in CI
└── tests/
    └── android_app/
        ├── conftest.py      # pytest fixtures, --platform, browser/driver setup
        ├── locators.py      # Platform-specific locators (Android / iOS)
        └── test_todo_app.py # Todo app test cases (TC1–TC10)
```

## Installation

```bash
git clone <repo-url>
cd test_automation_todo_app
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Install and start Appium (if not already):

```bash
npm install -g appium
appium driver install uiautomator2
appium
```

## Configuration

### Local runs – `config.py` and env

- **`config.py`** reads environment variables. Important ones:
  - `remote_url` – Appium server URL (default `http://127.0.0.1:4723`)
  - `android_deviceName` – device/emulator id; use `any` or `any_active` to auto-pick the first from `adb devices` (CI sets this from `ci/config.yaml`)
  - `android_app` – optional path to APK to install before the run

You can also pass the device via **pytest**: `--device <id>` or `--device any` (see [Running tests](#running-tests)). Env is overridden by `--device` when building the driver.

Override locally with env, for example:

```powershell
$env:android_deviceName = "emulator-5554"
$env:remote_url = "http://127.0.0.1:4723"
```

### CI – `ci/config.yaml`

- **platform**: `android` or `ios`
- **device**: `any_active` (first connected emulator/device) or a specific id (e.g. `emulator-5554`)

The workflow exports these so the run uses the chosen device, not the default in `config.py`. See [ci/README.md](ci/README.md) for APK and manual run details.

## Running tests

From the project root with the virtual environment activated:

**All Todo app tests (Android)** (device from env or first from `adb devices`):

```bash
pytest tests/android_app/test_todo_app.py --platform android
```

**With a specific device** (or `any` / `any_active` to use the first connected):

```bash
pytest tests/android_app/test_todo_app.py --platform android --device emulator-5554
pytest tests/android_app/test_todo_app.py --platform android --device any
```

**Single test:**

```bash
pytest tests/android_app/test_todo_app.py::test_tc1_create_task_happy_path --platform android
```

**With options:**

```bash
pytest tests/android_app/test_todo_app.py --platform android --device emulator-5554 -v --tb=short
```

**iOS** (mock locators; real device/simulator needed for real runs):

```bash
pytest tests/android_app/test_todo_app.py --platform ios
```

## Test cases (overview)

| ID  | Description |
|-----|-------------|
| TC1 | Create a new task (happy path) |
| TC2 | Create multiple tasks and verify listing |
| TC3 | Mark task completed and verify Completed/Active filters |
| TC4 | Filter All / Active / Completed |
| TC5 | Clear completed tasks |
| TC6 | Refresh keeps current state |
| TC7 | Navigate to Statistics and back to Task List |
| TC8 | Statistics percentages reflect task data |
| TC9 | Cannot save an empty task (validation) |
| TC10 | Regression: white-screen bug after New Task → Back → Drawer (xfail) |


## CI pipeline

- **Workflow**: [.github/workflows/android-tests.yml](.github/workflows/android-tests.yml)
- **Triggers**: manual **Run workflow** only
- **Behaviour**: Reads `ci/config.yaml` (or manual inputs), starts an Android emulator, starts Appium, sets `android_deviceName` from config, and runs pytest with `--platform` and `--device` so the same parametrization is used as locally. Device in use is printed in the log (`Using device (android_deviceName): ...`).
- **APK**: For the app to be installed in CI, place `todo.apk` at `ci/todo.apk` or adjust the workflow (see [ci/README.md](ci/README.md)).

## License / repo

Part of the test automation assignment; repository as per your setup.
