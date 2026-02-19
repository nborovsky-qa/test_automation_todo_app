"""
Conftest for Todo-app tests.

Run with:
    pytest tests/android_app/test_todo_app.py --platform android
    pytest tests/android_app/test_todo_app.py --platform android --device emulator-5554
    pytest tests/android_app/test_todo_app.py --platform android --device any
    pytest tests/android_app/test_todo_app.py --platform ios
"""

import os
import sys
from pathlib import Path

# Ensure project root and this package are on path so config and locators import
_project_root = Path(__file__).resolve().parent.parent.parent
_android_app_dir = Path(__file__).resolve().parent
for _path in (_project_root, _android_app_dir):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import pytest
from appium import webdriver
from selene import browser

import config
from locators import get_locators


def pytest_addoption(parser):
    parser.addoption(
        '--platform',
        action='store',
        default='android',
        choices=['android', 'ios'],
        help='Target mobile platform: Android (UIAutomator2) or iOS (XCUITest)',
    )
    parser.addoption(
        '--device',
        action='store',
        default='',
        help='Device id for Appium (e.g. emulator-5554, R5CT4037HVT). '
             'Use "any" or "any_active" to pick the first from adb devices. '
             'Default: use env android_deviceName or first connected device.',
    )


@pytest.fixture(scope='session')
def platform(request):
    # The target mobile platform selected via --platform CLI option
    return request.config.getoption('--platform')


@pytest.fixture(scope='session')
def device(request):
    # Device id or any/any_active from --device CLI option
    return request.config.getoption('--device', default='')


@pytest.fixture(scope='session')
def locators(platform):
    # Locator class matching the active platform (AndroidLocators / iOSLocators)
    return get_locators(platform)


@pytest.fixture(scope='function', autouse=True)
def mobile_management(platform, device):
    # Set up the Appium driver via selene's browser before each test and quit after.
    remote_url = (
        config.ANDROID_REMOTE_URL
        if platform.lower() == 'android'
        else config.IOS_REMOTE_URL
    )
    browser.config.driver = webdriver.Remote(
        remote_url,
        options=config.todo_driver_options(platform, device_override=device or None),
    )
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    browser.quit()
