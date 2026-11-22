import allure
from selenium.common.exceptions import TimeoutException

from data import ORDER_NUMBER_PLACEHOLDER, Urls
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    ORDER_TIMEOUT = 40

    @allure.step("Открыть главную страницу (конструктор)")
    def open_page(self):
        self.open(Urls.MAIN)
        self.find_visible(MainPageLocators.BUN_CARD)

    @allure.step("Проверить, что открыт конструктор")
    def is_constructor_opened(self):
        return self.is_visible(MainPageLocators.TITLE)

    @allure.step("Дождаться кнопки «Оформить заказ» (пользователь авторизован)")
    def wait_order_button(self):
        self.find_visible(MainPageLocators.ORDER_BUTTON)

    @allure.step("Получить название первой булки")
    def get_bun_name(self):
        return self.get_text(MainPageLocators.BUN_NAME)

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self):
        self.click(MainPageLocators.BUN_CARD)

    @allure.step("Дождаться открытия окна с деталями ингредиента")
    def wait_ingredient_modal_opened(self):
        self.find_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    @allure.step("Проверить, что окно с деталями ингредиента открыто")
    def is_ingredient_modal_opened(self):
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    @allure.step("Получить название ингредиента в модальном окне")
    def get_modal_ingredient_name(self):
        return self.get_text(MainPageLocators.INGREDIENT_MODAL_NAME)

    @allure.step("Проверить отображение БЖУ/калорий в окне ингредиента")
    def is_ingredient_modal_stats_visible(self):
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL_STATS)

    @allure.step("Закрыть всплывающее окно крестиком")
    def close_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON, wait_overlays=False)

    @allure.step("Дождаться закрытия всплывающего окна")
    def wait_modal_closed(self):
        self.wait_invisible(MainPageLocators.OPENED_MODAL)
        return self.wait_overlays_invisible()

    @allure.step("Проверить, что всплывающее окно закрыто")
    def is_modal_closed(self):
        try:
            return self.wait_modal_closed()
        except TimeoutException:
            return False

    @allure.step("Получить значение счётчика булки")
    def get_bun_counter(self):
        return int(self.get_text(MainPageLocators.BUN_COUNTER))

    @allure.step("Получить значение счётчика начинки")
    def get_filling_counter(self):
        return int(self.get_text(MainPageLocators.FILLING_COUNTER))

    @allure.step("Добавить булку в заказ")
    def add_bun_to_order(self):
        before = self.get_bun_counter()
        self.drag_and_drop(MainPageLocators.BUN_CARD, MainPageLocators.BASKET)

        def counter_changed(_):
            text = self.get_text_now(MainPageLocators.BUN_COUNTER)
            return text is not None and text.isdigit() and int(text) != before

        self.wait().until(counter_changed)

    @allure.step("Добавить начинку в заказ")
    def add_filling_to_order(self):
        before = self.get_filling_counter()
        self.drag_and_drop(MainPageLocators.FILLING_CARD, MainPageLocators.BASKET)

        def counter_changed(_):
            text = self.get_text_now(MainPageLocators.FILLING_COUNTER)
            return text is not None and text.isdigit() and int(text) != before

        self.wait().until(counter_changed)

    @allure.step("Нажать «Оформить заказ»")
    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Получить номер оформленного заказа")
    def get_order_number(self):
        self.find_visible(MainPageLocators.ORDER_NUMBER, self.ORDER_TIMEOUT)

        def real_number(_):
            text = self.get_text_now(MainPageLocators.ORDER_NUMBER)
            if text and text not in ("", ORDER_NUMBER_PLACEHOLDER):
                return text
            return False

        return self.wait(self.ORDER_TIMEOUT).until(real_number)

    @allure.step("Собрать бургер и оформить заказ")
    def make_order(self):
        self.add_bun_to_order()
        self.add_filling_to_order()
        self.click_order_button()
        number = self.get_order_number()
        self.close_modal()
        self.wait_modal_closed()
        return number
