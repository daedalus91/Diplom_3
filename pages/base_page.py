import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seletools.actions import drag_and_drop as seletools_drag_and_drop

from data import ACTIVE_LINK_CLASS
from locators.base_page_locators import BasePageLocators


class BasePage:
    TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def set_auth_tokens(self, access_token, refresh_token):
        with allure.step("Установить токены авторизации в localStorage"):
            self.driver.execute_script(
                "window.localStorage.setItem('accessToken', arguments[0]);"
                "window.localStorage.setItem('refreshToken', arguments[1]);",
                access_token,
                refresh_token,
            )

    def wait(self, timeout=None, ignored_exceptions=(StaleElementReferenceException,)):
        return WebDriverWait(
            self.driver, timeout or self.TIMEOUT, ignored_exceptions=ignored_exceptions
        )

    def find_visible(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_invisible(self, locator, timeout=None):
        return bool(self.wait(timeout).until(EC.invisibility_of_element_located(locator)))

    def wait_all_invisible(self, locator, timeout=None):
        def all_hidden(_):
            try:
                elements = self.driver.find_elements(*locator)
                return all(not el.is_displayed() for el in elements)
            except StaleElementReferenceException:
                return False

        return bool(self.wait(timeout).until(all_hidden))

    def wait_loading_modal_invisible(self, timeout=None):
        return self.wait_all_invisible(BasePageLocators.LOADING_MODAL, timeout)

    def wait_overlays_invisible(self, timeout=None):
        return self.wait_all_invisible(BasePageLocators.MODAL_OVERLAY, timeout)

    def is_visible(self, locator, timeout=None):
        try:
            return self.find_visible(locator, timeout).is_displayed()
        except TimeoutException:
            return False

    def click(self, locator, timeout=None, wait_overlays=True):
        self.wait_loading_modal_invisible(timeout)
        if wait_overlays:
            self.wait_overlays_invisible(timeout)
        element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def get_text(self, locator, timeout=None):
        return self.find_visible(locator, timeout).text

    def get_text_now(self, locator):
        try:
            elements = self.driver.find_elements(*locator)
            if elements and elements[0].is_displayed():
                return elements[0].text
        except StaleElementReferenceException:
            return None
        return None

    def wait_url(self, url, timeout=None):
        return self.wait(timeout).until(EC.url_to_be(url))

    def current_url(self):
        return self.driver.current_url

    def drag_and_drop(self, source_locator, target_locator):
        source = self.find_visible(source_locator)
        target = self.find_visible(target_locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", source)
        seletools_drag_and_drop(self.driver, source, target)

    @allure.step("Кликнуть «Конструктор» в шапке")
    def click_constructor_link(self):
        self.click(BasePageLocators.CONSTRUCTOR_LINK)

    @allure.step("Проверить, активна ли вкладка «Конструктор»")
    def is_constructor_link_active(self):
        css_class = self.find_visible(BasePageLocators.CONSTRUCTOR_LINK).get_attribute("class") or ""
        return ACTIVE_LINK_CLASS in css_class

    @allure.step("Кликнуть «Лента Заказов» в шапке")
    def click_feed_link(self):
        self.click(BasePageLocators.FEED_LINK)
