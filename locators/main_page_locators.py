from selenium.webdriver.common.by import By


class MainPageLocators:
    TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

    BUN_CARD = (
        By.XPATH,
        "//h2[text()='Булки']/following-sibling::ul[1]"
        "//a[contains(@class,'BurgerIngredient_ingredient__')][1]",
    )
    BUN_NAME = (
        By.XPATH,
        "//h2[text()='Булки']/following-sibling::ul[1]"
        "//a[contains(@class,'BurgerIngredient_ingredient__')][1]"
        "//p[contains(@class,'BurgerIngredient_ingredient__text')]",
    )
    BUN_COUNTER = (
        By.XPATH,
        "//h2[text()='Булки']/following-sibling::ul[1]"
        "//a[contains(@class,'BurgerIngredient_ingredient__')][1]"
        "//p[contains(@class,'counter_counter__num')]",
    )
    FILLING_CARD = (
        By.XPATH,
        "//h2[text()='Начинки']/following-sibling::ul[1]"
        "//a[contains(@class,'BurgerIngredient_ingredient__')][1]",
    )
    FILLING_COUNTER = (
        By.XPATH,
        "//h2[text()='Начинки']/following-sibling::ul[1]"
        "//a[contains(@class,'BurgerIngredient_ingredient__')][1]"
        "//p[contains(@class,'counter_counter__num')]",
    )

    BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    OPENED_MODAL = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened']")
    INGREDIENT_MODAL_TITLE = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//h2[text()='Детали ингредиента']",
    )
    INGREDIENT_MODAL_NAME = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//ul[contains(@class,'Modal_modal__statsList')]/preceding-sibling::p[1]",
    )
    INGREDIENT_MODAL_STATS = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] ul[class*='Modal_modal__statsList']",
    )
    MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] button[class*='Modal_modal__close']",
    )
    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] h2[class*='Modal_modal__title']",
    )
