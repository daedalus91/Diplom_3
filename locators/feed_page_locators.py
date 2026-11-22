from selenium.webdriver.common.by import By


class FeedPageLocators:
    TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_LIST = (By.CSS_SELECTOR, "ul[class*='OrderFeed_orderListReady']")
