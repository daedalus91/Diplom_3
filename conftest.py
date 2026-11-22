import os

import allure
import pytest
from selenium import webdriver

from helpers import delete_user, generate_user, register_user
from pages.feed_page import FeedPage
from pages.main_page import MainPage

HEADLESS = os.getenv("HEADLESS", "").lower() in ("1", "true", "yes")
SUPPORTED_BROWSERS = ("chrome", "firefox")


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=("all", *SUPPORTED_BROWSERS),
        help="Браузер для запуска тестов: chrome, firefox или all (по умолчанию: all)",
    )


def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        option = metafunc.config.getoption("--browser")
        browsers = list(SUPPORTED_BROWSERS) if option == "all" else [option]
        metafunc.parametrize("browser", browsers)


def _create_driver(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.set_window_size(1920, 1080)
    return driver


@pytest.fixture
def driver(browser):
    web_driver = _create_driver(browser)
    yield web_driver
    web_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    web_driver = item.funcargs.get("driver")
    if report.when in ("setup", "call") and report.failed and web_driver:
        try:
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


@pytest.fixture
def feed_page(driver):
    return FeedPage(driver)


@pytest.fixture
def opened_main_page(main_page):
    main_page.open_page()
    return main_page


@pytest.fixture
def opened_feed_page(feed_page):
    feed_page.open_page()
    return feed_page


@pytest.fixture
def user():
    payload = generate_user()
    tokens = register_user(payload)
    yield {**payload, **tokens}
    delete_user(tokens["access_token"])


@pytest.fixture
def authorized_main_page(opened_main_page, user):
    opened_main_page.set_auth_tokens(user["access_token"], user["refresh_token"])
    opened_main_page.refresh()
    opened_main_page.wait_order_button()
    return opened_main_page
