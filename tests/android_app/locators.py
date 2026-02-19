from appium.webdriver.common.appiumby import AppiumBy

# Platform-specific element locators
class AndroidLocators:
    # content-desc="Open Drawer"
    OPEN_DRAWER = (AppiumBy.ACCESSIBILITY_ID, 'Open Drawer')
    # content-desc="Filter"
    FILTER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Filter')
    # content-desc="More"
    MORE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'More')
    # content-desc="New Task"
    NEW_TASK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'New Task')
    # empty state white screen
    EMPTY_STATE_WHITE_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/content")')

    # Task List content
    EMPTY_STATE_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("You have no tasks!")',
    )

    # Filter dropdown (appears after tapping FILTER_BUTTON)
    FILTER_ALL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("All")')
    FILTER_ACTIVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Active")')
    FILTER_COMPLETED_OPTION = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Completed")',
    )

    # Overflow menu (appears after tapping MORE_BUTTON)
    MENU_CLEAR_COMPLETED = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Clear completed")',
    )
    MENU_REFRESH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Refresh")')



    # Navigation drawer (appears after tapping OPEN_DRAWER)
    NAV_TASK_LIST = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Task List")',
    )
    NAV_STATISTICS = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Statistics")',
    )


    # New Task screen
    # content-desc="Back"
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Back')
    # content-desc="Save task"
    SAVE_TASK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Save task')
    # accessibility tree: instance(0) = Title field, instance(1) = Description.
    TASK_TITLE_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)',
    )
    TASK_DESC_INPUT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(1)',
    )


    # Statistics screen
    STATS_ACTIVE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textStartsWith("Active tasks:")',
    )
    STATS_COMPLETED = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textStartsWith("Completed tasks:")',
    )

    # Validation snackbar
    # Shown when user tries to save a task with an empty title
    SNACKBAR_EMPTY_TASK = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("empty")',
    )

    # Dynamic locators
    @staticmethod
    def task_by_title(title: str) -> tuple:
    # Locate a task row by its visible title text
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{title}")',
        )

    @staticmethod
    def task_checkbox_by_title(title: str) -> tuple:
        # Locate the ccheckbox in the same task row as the given title.
        return (
            AppiumBy.XPATH,
            (
                '//android.view.View'
                f'[./android.widget.CheckBox]'
                f'[./android.widget.TextView[@text="{title}"]]'
                '/android.widget.CheckBox'
            ),
        )


# Mocked iOS locators
class iOSLocators:

    # Toolbar
    OPEN_DRAWER = (AppiumBy.ACCESSIBILITY_ID, 'Open Drawer')
    FILTER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Filter')
    MORE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'More')
    NEW_TASK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'New Task')

    # Task List content
    EMPTY_STATE_TEXT = (AppiumBy.ACCESSIBILITY_ID, 'You have no tasks!')

    # Filter dropdown
    FILTER_ALL = (AppiumBy.XPATH, '//*[@name="All"]')
    FILTER_ACTIVE = (AppiumBy.XPATH, '//*[@name="Active"]')
    FILTER_COMPLETED_OPTION = (AppiumBy.XPATH, '//*[@name="Completed"]')

    # Overflow menu
    MENU_CLEAR_COMPLETED = (AppiumBy.ACCESSIBILITY_ID, 'Clear completed')
    MENU_REFRESH = (AppiumBy.ACCESSIBILITY_ID, 'Refresh')

    # Navigation drawer
    NAV_TASK_LIST = (AppiumBy.ACCESSIBILITY_ID, 'Task List')
    NAV_STATISTICS = (AppiumBy.ACCESSIBILITY_ID, 'Statistics')

    # New Task screen
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Back')
    SAVE_TASK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Save task')
    TASK_TITLE_INPUT = (AppiumBy.XPATH, '//XCUIElementTypeTextField[1]')
    TASK_DESC_INPUT = (AppiumBy.XPATH, '//XCUIElementTypeTextView[1]')

    # Statistics screen
    STATS_ACTIVE = (
        AppiumBy.XPATH,
        '//XCUIElementTypeStaticText[contains(@name, "Active tasks:")]',
    )
    STATS_COMPLETED = (
        AppiumBy.XPATH,
        '//XCUIElementTypeStaticText[contains(@name, "Completed tasks:")]',
    )

    # Validation
    SNACKBAR_EMPTY_TASK = (
        AppiumBy.XPATH,
        '//*[contains(@name, "empty")]',
    )

    # Dynamic locators
    @staticmethod
    def task_by_title(title: str) -> tuple:
        return (AppiumBy.ACCESSIBILITY_ID, title)

    @staticmethod
    def task_checkbox_by_title(title: str) -> tuple:
        return (
            AppiumBy.XPATH,
            (
                '//XCUIElementTypeCell['
                f'.//XCUIElementTypeStaticText[@name="{title}"]'
                ']//XCUIElementTypeButton'
            ),
        )


def get_locators(platform: str):
    # Return the locator class for the given platform name
    p = platform.lower()
    if p == 'android':
        return AndroidLocators
    if p == 'ios':
        return iOSLocators
    raise ValueError(f'Unsupported platform: {platform!r}')
