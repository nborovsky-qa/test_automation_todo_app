"""
Automated tests for the Todo mobile app (Android / iOS via Appium).

Run:
    pytest tests/android_app/test_todo_app.py --platform android
    pytest tests/android_app/test_todo_app.py --platform ios   # mock / no device
"""

import re
import time

import pytest
from selene import browser, be, have



# App-level helpers
def create_task(locators, title: str, description: str = '') -> None:
    """Open New Task screen, fill both fields, dismiss keyboard, and save.

    Both fields are always filled; when no description is supplied it defaults
    to the title text, preventing the 'Tasks cannot be empty' validation error.
    """
    browser.element(locators.NEW_TASK_BUTTON).click()
    browser.element(locators.TASK_TITLE_INPUT).type(title)
    browser.element(locators.TASK_DESC_INPUT).type(description if description else title)
    try:
        browser.driver.hide_keyboard()
    except Exception:
        pass
    browser.element(locators.SAVE_TASK_BUTTON).click()


def mark_task_complete(locators, title: str) -> None:
    """Tick the checkbox next to the given task title.

    A short pause after tapping lets the Compose UI commit the completion
    state before any subsequent action (e.g. 'Clear completed') reads it.
    """
    browser.element(locators.task_checkbox_by_title(title)).click()
    time.sleep(1)


def select_filter(locators, filter_locator) -> None:
    """Open the filter (pyramid) menu and pick an option."""
    browser.element(locators.FILTER_BUTTON).click()
    browser.element(filter_locator).click()


def open_overflow(locators, option_locator) -> None:
    """Open the overflow (three-dots) menu and select a menu item."""
    browser.element(locators.MORE_BUTTON).click()
    browser.element(option_locator).click()


def go_to_statistics(locators) -> None:
    """Open the navigation drawer and navigate to Statistics."""
    browser.element(locators.OPEN_DRAWER).click()
    browser.element(locators.NAV_STATISTICS).click()


def go_to_task_list(locators) -> None:
    """Open the navigation drawer and navigate back to Task List."""
    browser.element(locators.OPEN_DRAWER).click()
    browser.element(locators.NAV_TASK_LIST).click()


# Test cases

@pytest.mark.name('Create a new task')
@pytest.mark.test_case_id('id1')
def test_tc1_create_task_happy_path(locators):
    """
    Given the initial page shows the empty state,
    when the user creates a task with a title and description,
    then the task appears in the list and the empty state is gone.
    """
    browser.element(locators.EMPTY_STATE_TEXT).should(be.visible)

    create_task(locators, title='Buy groceries', description='Milk, eggs, bread')

    browser.element(locators.task_by_title('Buy groceries')).should(be.visible)
    browser.all(locators.EMPTY_STATE_TEXT).should(have.size(0))



@pytest.mark.name('Create multiple tasks')
@pytest.mark.test_case_id('id2')
def test_tc2_create_multiple_tasks(locators):
    """
    When the user creates three tasks with different titles,
    all three are visible in the task list.
    """
    titles = ['Task Alpha', 'Task Beta', 'Task Gamma']

    for title in titles:
        create_task(locators, title=title)

    for title in titles:
        browser.element(locators.task_by_title(title)).should(be.visible)


@pytest.mark.name('Mark task as completed and verify filters')
@pytest.mark.test_case_id('id3')
def test_tc3_mark_task_completed_and_verify_filters(locators):
    """
    Given one active task, when the user marks it as completed,
    it appears under the Completed filter and is absent from Active.
    """
    create_task(locators, title='Finish report')
    mark_task_complete(locators, title='Finish report')

    select_filter(locators, locators.FILTER_COMPLETED_OPTION)
    browser.element(locators.task_by_title('Finish report')).should(be.visible)

    select_filter(locators, locators.FILTER_ACTIVE)
    browser.all(locators.task_by_title('Finish report')).should(have.size(0))



@pytest.mark.name('Filter "All" / "Active" / "Completed"')
@pytest.mark.test_case_id('id4')
def test_tc4_filter_all_active_completed(locators):
    """
    Given two tasks (one active, one completed),
    the All filter shows both, Active shows one, Completed shows one.
    """
    create_task(locators, title='Active task')
    create_task(locators, title='Done task')
    mark_task_complete(locators, title='Done task')

    select_filter(locators, locators.FILTER_ALL)
    browser.element(locators.task_by_title('Active task')).should(be.visible)
    browser.element(locators.task_by_title('Done task')).should(be.visible)

    select_filter(locators, locators.FILTER_ACTIVE)
    browser.element(locators.task_by_title('Active task')).should(be.visible)
    browser.all(locators.task_by_title('Done task')).should(have.size(0))

    select_filter(locators, locators.FILTER_COMPLETED_OPTION)
    browser.element(locators.task_by_title('Done task')).should(be.visible)
    browser.all(locators.task_by_title('Active task')).should(have.size(0))


@pytest.mark.name('Clear completed tasks')
@pytest.mark.test_case_id('id5')
def test_tc5_clear_completed_tasks(locators):
    """
    Given one active and one completed task,
    when the user selects 'Clear completed',
    the completed task is removed and the active task remains.
    """
    create_task(locators, title='Keep me')
    create_task(locators, title='Remove me')
    mark_task_complete(locators, title='Remove me')

    open_overflow(locators, locators.MENU_CLEAR_COMPLETED)

    browser.all(locators.task_by_title('Remove me')).should(have.size(0))
    browser.element(locators.task_by_title('Keep me')).should(be.visible)


@pytest.mark.name('Refresh keeps current state')
@pytest.mark.test_case_id('id6')
def test_tc6_refresh_keeps_state(locators):
    """
    Given tasks with mixed completion states,
    selecting Refresh from the overflow menu preserves all tasks and states.
    """
    create_task(locators, title='Still active')
    create_task(locators, title='Already done')
    mark_task_complete(locators, title='Already done')

    open_overflow(locators, locators.MENU_REFRESH)

    browser.element(locators.task_by_title('Still active')).should(be.visible)
    browser.element(locators.task_by_title('Already done')).should(be.visible)

    select_filter(locators, locators.FILTER_COMPLETED_OPTION)
    browser.element(locators.task_by_title('Already done')).should(be.visible)



@pytest.mark.name('Navigate to Statistics and back to Task List')
@pytest.mark.test_case_id('id7')
def test_tc7_navigate_to_statistics_and_back(locators):
    """
    When the user opens the drawer and taps Statistics, the Statistics view
    is shown.  When tapping Task List, the task list is restored with
    previously created tasks intact.
    """
    create_task(locators, title='Navigation test task')

    go_to_statistics(locators)
    browser.element(locators.STATS_ACTIVE).should(be.visible)
    browser.element(locators.STATS_COMPLETED).should(be.visible)

    go_to_task_list(locators)
    browser.element(locators.task_by_title('Navigation test task')).should(be.visible)



@pytest.mark.name('Statistics percentages reflect actual task data')
@pytest.mark.test_case_id('id8')
def test_tc8_statistics_reflect_task_data(locators):
    """
    Given two tasks with one completed (50 % each),
    the Statistics view reports 50 % Active and 50 % Completed.
    """
    create_task(locators, title='Stats task 1')
    create_task(locators, title='Stats task 2')
    mark_task_complete(locators, title='Stats task 1')

    go_to_statistics(locators)

    active_stats = browser.element(locators.STATS_ACTIVE)
    active_stats.should(be.visible)
    active_text = active_stats.locate().text

    completed_stats = browser.element(locators.STATS_COMPLETED)
    completed_stats.should(be.visible)
    completed_text = completed_stats.locate().text

    active_match = re.search(r'(\d+\.?\d*)%', active_text)
    assert active_match, f'Could not parse percentage from: {active_text!r}'
    active_pct = float(active_match.group(1))
    assert abs(active_pct - 50.0) < 1.0, (
        f'Expected 50 % active tasks, got {active_pct} %'
    )

    completed_match = re.search(r'(\d+\.?\d*)%', completed_text)
    assert completed_match, f'Could not parse percentage from: {completed_text!r}'
    completed_pct = float(completed_match.group(1))
    assert abs(completed_pct - 50.0) < 1.0, (
        f'Expected 50 % completed tasks, got {completed_pct} %'
    )


@pytest.mark.name('Cannot save an empty task')
@pytest.mark.test_case_id('id9')
def test_tc9_cannot_save_empty_task(locators):
    """
    When the user opens New Task, leaves all fields empty and taps Save,
    an error message is shown and no task is added to the list.
    """
    browser.element(locators.NEW_TASK_BUTTON).click()
    browser.element(locators.SAVE_TASK_BUTTON).click()

    browser.element(locators.SNACKBAR_EMPTY_TASK).should(be.visible)

    browser.element(locators.BACK_BUTTON).click()

    browser.element(locators.EMPTY_STATE_TEXT).should(be.visible)



@pytest.mark.name('Regression: known white-screen bug')
@pytest.mark.test_case_id('id10')
@pytest.mark.xfail(
    reason=(
        'Known bug: navigation drawer shows white screen after '
        'New Task → Back → Open Drawer sequence.'
    ),
    strict=False,
)
def test_tc10_white_screen_bug_regression(locators):
    """
    Known bug (?): after opening New Task and tapping Back, opening the navigation
    drawer produces a white screen instead of the menu.

    Expected (future fixed state): the drawer shows 'Task List' and 'Statistics'.
    Current state: FAILS
    """
    browser.element(locators.NEW_TASK_BUTTON).click()
    browser.element(locators.BACK_BUTTON).click()
    browser.element(locators.OPEN_DRAWER).click()
    
    browser.element(locators.NAV_TASK_LIST).should(be.visible)
    browser.element(locators.NAV_STATISTICS).should(be.visible)

    browser.element(locators.EMPTY_STATE_WHITE_SCREEN).should(be.hidden)
