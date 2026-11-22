import allure
from selenium.common.exceptions import TimeoutException

from data import Urls
from locators.feed_page_locators import FeedPageLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    UPDATE_TIMEOUT = 30

    @allure.step("Открыть страницу «Лента заказов»")
    def open_page(self):
        self.open(Urls.FEED)
        self.find_visible(FeedPageLocators.TOTAL_COUNTER)

    @allure.step("Проверить, что открыта «Лента заказов»")
    def is_feed_opened(self):
        return self.is_visible(FeedPageLocators.TITLE)

    @allure.step("Получить счётчик «Выполнено за всё время»")
    def get_total_counter(self):
        return int(self.get_text(FeedPageLocators.TOTAL_COUNTER))

    @allure.step("Получить счётчик «Выполнено за сегодня»")
    def get_today_counter(self):
        return int(self.get_text(FeedPageLocators.TODAY_COUNTER))

    def _wait_counter_increased(self, locator, previous):
        def counter_increased(_):
            text = self.get_text_now(locator)
            return text is not None and text.isdigit() and int(text) > previous

        try:
            self.wait(self.UPDATE_TIMEOUT).until(counter_increased)
        except TimeoutException:
            pass
        return int(self.get_text(locator))

    @allure.step("Дождаться увеличения счётчика «Выполнено за всё время»")
    def wait_total_counter_increased(self, previous):
        return self._wait_counter_increased(FeedPageLocators.TOTAL_COUNTER, previous)

    @allure.step("Дождаться увеличения счётчика «Выполнено за сегодня»")
    def wait_today_counter_increased(self, previous):
        return self._wait_counter_increased(FeedPageLocators.TODAY_COUNTER, previous)

    @allure.step("Дождаться появления заказа {order_number} в разделе «В работе»")
    def wait_for_order_in_progress(self, order_number):
        """Ждёт появления номера в списке «В работе» и возвращает актуальный список номеров."""
        expected = int(order_number)

        def current_numbers():
            text = self.get_text_now(FeedPageLocators.IN_PROGRESS_LIST) or ""
            return [int(item) for item in text.split() if item.isdigit()]

        try:
            self.wait(self.UPDATE_TIMEOUT).until(lambda _: expected in current_numbers())
        except TimeoutException:
            pass
        return current_numbers()
