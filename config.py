# Android Config

import os

ANDROID_REMOTE_URL = os.getenv('remote_url', 'http://127.0.0.1:4723')
# Default is for local run. CI sets android_deviceName from YAML
ANDROID_DEVICE_NAME = os.getenv('android_deviceName', 'samsung SM-S908B')
ANDROID_APP_PACKAGE = os.getenv(
    'android_appPackage',
    'com.example.android.architecture.blueprints.main',
)
ANDROID_APP_ACTIVITY = os.getenv(
    'android_appActivity',
    'com.example.android.architecture.blueprints.todoapp.TodoActivity',
)
ANDROID_APP_WAIT_ACTIVITY = os.getenv(
    'android_appWaitActivity',
    'com.example.android.architecture.blueprints.*',
)
# Leave empty to launch the already-installed app without reinstalling.
# Set android_app env var to an APK path when you want Appium to (re)install it.
ANDROID_APP_PATH = os.getenv('android_app', '')


def _android_options():
    from appium.options.android import UiAutomator2Options
    options = UiAutomator2Options()
    options.set_capability('deviceName', ANDROID_DEVICE_NAME)
    options.set_capability('appPackage', ANDROID_APP_PACKAGE)
    options.set_capability('appActivity', ANDROID_APP_ACTIVITY)
    options.set_capability('appWaitActivity', ANDROID_APP_WAIT_ACTIVITY)
    if ANDROID_APP_PATH:
        options.set_capability('app', ANDROID_APP_PATH)
    options.set_capability('noReset', False)
    options.set_capability('autoGrantPermissions', True)
    return options


# iOS Config
# These values are intentionally placeholder

IOS_REMOTE_URL = os.getenv('remote_url', 'http://127.0.0.1:4723')
IOS_DEVICE_NAME = os.getenv('ios_deviceName', 'iPhone Air')
IOS_PLATFORM_VERSION = os.getenv('ios_platformVersion', '23.0')
IOS_BUNDLE_ID = os.getenv('ios_bundleId', 'com.example.todo')
IOS_APP_PATH = os.getenv('ios_app', '/path/to/Todo.app')


def _ios_options():
    from appium.options.ios import XCUITestOptions
    options = XCUITestOptions()
    options.set_capability('deviceName', IOS_DEVICE_NAME)
    options.set_capability('platformVersion', IOS_PLATFORM_VERSION)
    options.set_capability('bundleId', IOS_BUNDLE_ID)
    options.set_capability('app', IOS_APP_PATH)
    options.set_capability('automationName', 'XCUITest')
    options.set_capability('noReset', False)
    return options


def todo_driver_options(platform: str = 'android'):
    """Return Appium capability options for the Todo app on the given platform.

    Usage::

        pytest --platform android   # UIAutomator2 + Android config
        pytest --platform ios       # XCUITest    + iOS config (mock)
    """
    p = platform.lower()
    if p == 'android':
        return _android_options()
    if p == 'ios':
        return _ios_options()
    raise ValueError(f'Unsupported platform: {platform!r}')

