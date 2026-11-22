from selenium.webdriver.common.by import By


class BasePageLocators:
    CONSTRUCTOR_LINK = (By.CSS_SELECTOR, "header a[class*='AppHeader_header__link__'][href='/']")
    FEED_LINK = (By.CSS_SELECTOR, "header a[href='/feed']")
    LOADING_MODAL = (
        By.XPATH,
        "//div[contains(@class,'Modal_modal__')][.//img[contains(@class,'Modal_modal__loading')]]",
    )
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")
