import allure

from data import Urls


@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор» открывает раздел конструктора")
    def test_go_to_constructor_opens_constructor_section(self, opened_feed_page, main_page):
        opened_feed_page.click_constructor_link()
        main_page.wait_url(Urls.MAIN)
        is_opened = main_page.is_constructor_opened()

        assert is_opened, "После клика на «Конструктор» заголовок конструктора не отобразился"

    @allure.title("Переход по клику на «Конструктор» обновляет URL на главную страницу")
    def test_go_to_constructor_updates_url(self, opened_feed_page, main_page):
        opened_feed_page.click_constructor_link()
        main_page.wait_url(Urls.MAIN)
        current_url = main_page.current_url()

        assert current_url == Urls.MAIN, (
            f"Ожидался URL {Urls.MAIN}, получено: {current_url}"
        )

    @allure.title("Переход по клику на «Конструктор» делает вкладку активной")
    def test_go_to_constructor_activates_header_link(self, opened_feed_page, main_page):
        opened_feed_page.click_constructor_link()
        main_page.wait_url(Urls.MAIN)
        is_active = main_page.is_constructor_link_active()

        assert is_active, "После перехода на «Конструктор» ссылка в шапке не стала активной"

    @allure.title("Переход по клику на «Лента заказов» открывает раздел ленты")
    def test_go_to_order_feed_opens_feed_section(self, opened_main_page, feed_page):
        opened_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        is_opened = feed_page.is_feed_opened()

        assert is_opened, "После клика на «Лента Заказов» заголовок ленты не отобразился"

    @allure.title("Переход по клику на «Лента заказов» обновляет URL на /feed")
    def test_go_to_order_feed_updates_url(self, opened_main_page, feed_page):
        opened_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        current_url = feed_page.current_url()

        assert current_url == Urls.FEED, (
            f"Ожидался URL {Urls.FEED}, получено: {current_url}"
        )

    @allure.title("Клик на ингредиент открывает окно с деталями")
    def test_click_ingredient_opens_details_modal(self, opened_main_page):
        opened_main_page.click_ingredient()
        is_opened = opened_main_page.is_ingredient_modal_opened()

        assert is_opened, "Окно «Детали ингредиента» не открылось после клика на ингредиент"

    @allure.title("В окне деталей отображается название выбранного ингредиента")
    def test_ingredient_modal_displays_selected_ingredient_name(self, opened_main_page):
        expected_name = opened_main_page.get_bun_name()
        opened_main_page.click_ingredient()
        opened_main_page.wait_ingredient_modal_opened()
        actual_name = opened_main_page.get_modal_ingredient_name()

        assert actual_name == expected_name, (
            f"Ожидалось название ингредиента {expected_name!r}, получено: {actual_name!r}"
        )

    @allure.title("В окне деталей ингредиента отображаются калории и БЖУ")
    def test_ingredient_modal_displays_nutrition_stats(self, opened_main_page):
        opened_main_page.click_ingredient()
        opened_main_page.wait_ingredient_modal_opened()
        has_stats = opened_main_page.is_ingredient_modal_stats_visible()

        assert has_stats, "В окне «Детали ингредиента» не отображается блок калорий и БЖУ"

    @allure.title("Окно с деталями закрывается кликом по крестику")
    def test_close_ingredient_modal_by_cross(self, opened_main_page):
        opened_main_page.click_ingredient()
        opened_main_page.wait_ingredient_modal_opened()
        opened_main_page.close_modal()
        is_closed = opened_main_page.is_modal_closed()

        assert is_closed, "Всплывающее окно с деталями ингредиента не закрылось по клику на крестик"

    @allure.title("При добавлении булки в заказ её счётчик увеличивается на 2")
    def test_bun_counter_increases_after_adding(self, opened_main_page):
        counter_before = opened_main_page.get_bun_counter()
        opened_main_page.add_bun_to_order()
        counter_after = opened_main_page.get_bun_counter()

        assert counter_after == counter_before + 2, (
            f"Счётчик булки должен увеличиться на 2: было {counter_before}, стало {counter_after}"
        )

    @allure.title("При добавлении начинки в заказ её счётчик увеличивается на 1")
    def test_filling_counter_increases_after_adding(self, opened_main_page):
        counter_before = opened_main_page.get_filling_counter()
        opened_main_page.add_filling_to_order()
        counter_after = opened_main_page.get_filling_counter()

        assert counter_after == counter_before + 1, (
            f"Счётчик начинки должен увеличиться на 1: было {counter_before}, стало {counter_after}"
        )
