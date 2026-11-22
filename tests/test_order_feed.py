import allure

from data import Urls


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("После создания заказа счётчик «Выполнено за всё время» увеличивается")
    def test_total_counter_increases_after_new_order(self, authorized_main_page, feed_page):
        authorized_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        counter_before = feed_page.get_total_counter()

        feed_page.click_constructor_link()
        authorized_main_page.make_order()
        authorized_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        counter_after = feed_page.wait_total_counter_increased(counter_before)

        assert counter_after > counter_before, (
            f"Счётчик «Выполнено за всё время» не увеличился за {feed_page.UPDATE_TIMEOUT} с: "
            f"было {counter_before}, стало {counter_after}"
        )

    @allure.title("После создания заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_today_counter_increases_after_new_order(self, authorized_main_page, feed_page):
        authorized_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        counter_before = feed_page.get_today_counter()

        feed_page.click_constructor_link()
        authorized_main_page.make_order()
        authorized_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        counter_after = feed_page.wait_today_counter_increased(counter_before)

        assert counter_after > counter_before, (
            f"Счётчик «Выполнено за сегодня» не увеличился за {feed_page.UPDATE_TIMEOUT} с: "
            f"было {counter_before}, стало {counter_after}"
        )

    @allure.title("Номер оформленного заказа появляется в разделе «В работе»")
    def test_new_order_appears_in_progress(self, authorized_main_page, feed_page):
        order_number = authorized_main_page.make_order()
        authorized_main_page.click_feed_link()
        feed_page.wait_url(Urls.FEED)
        in_progress_orders = feed_page.wait_for_order_in_progress(order_number)

        assert int(order_number) in in_progress_orders, (
            f"Заказ #{order_number} не появился в разделе «В работе» за {feed_page.UPDATE_TIMEOUT} с; "
            f"текущий список: {in_progress_orders}"
        )
