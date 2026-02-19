# Android Config

import os
import subprocess
import re

ANDROID_REMOTE_URL = os.getenv('remote_url', 'http://127.0.0.1:4723')

# Default is for local run. CI sets android_deviceName from YAML.
# Set to empty, "any", or "any_active" to auto-pick the first device from `adb devices`.
_ANDROID_DEVICE_NAME_RAW = os.getenv('android_deviceName', 'any')


def _first_connected_android_device():
    # Return the first connected device/emulator id from `adb devices`, or None.
    try:
        out = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode != 0:
            return None
        # Lines like "emulator-5554" or "R5CT4037HVT"
        for line in out.stdout.splitlines():
            m = re.match(r'^(\S+)\s+device\s*$', line)
            if m:
                return m.group(1)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def get_android_device_name():
    # Device name for Appium: from env, or first connected device if env is any/any_active/empty
    raw = _ANDROID_DEVICE_NAME_RAW.strip().lower()
    if raw in ('', 'any', 'any_active'):
        device = _first_connected_android_device()
        return device if device else 'emulator-5554'
    return _ANDROID_DEVICE_NAME_RAW


ANDROID_DEVICE_NAME = get_android_device_name()
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


def _android_options(device_override=None):
    from appium.options.android import UiAutomator2Options
    if device_override is None or str(device_override).strip().lower() in ('', 'any', 'any_active'):
        device_name = get_android_device_name()
    else:
        device_name = str(device_override).strip()
    options = UiAutomator2Options()
    options.set_capability('deviceName', device_name)
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


def todo_driver_options(platform: str = 'android', device_override=None):
    """Return Appium capability options for the Todo app on the given platform.

    device_override: optional device id or 'any'/'any_active' (e.g. from pytest --device).
                     For Android, when None or any/any_active, uses env or first from adb.

    Usage::

        pytest --platform android                  # device from env or adb
        pytest --platform android --device emulator-5554
        pytest --platform ios
    """
    p = platform.lower()
    if p == 'android':
        return _android_options(device_override=device_override)
    if p == 'ios':
        return _ios_options()
    raise ValueError(f'Unsupported platform: {platform!r}')

