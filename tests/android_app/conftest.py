"""
Conftest for Todo-app tests.

Run with:
    pytest tests/android_app/test_todo_app.py --platform android
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


@pytest.fixture(scope='session')
def platform(request):
    # The target mobile platform selected via --platform CLI option
    return request.config.getoption('--platform')


@pytest.fixture(scope='session')
def locators(platform):
    # Locator class matching the active platform (AndroidLocators / iOSLocators)
    return get_locators(platform)


@pytest.fixture(scope='function', autouse=True)
def mobile_management(platform):
    # Set up the Appium driver via selene's browser before each test and quit after.
    remote_url = (
        config.ANDROID_REMOTE_URL
        if platform.lower() == 'android'
        else config.IOS_REMOTE_URL
    )
    browser.config.driver = webdriver.Remote(
        remote_url,
        options=config.todo_driver_options(platform),
    )
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    browser.quit()
