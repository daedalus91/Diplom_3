# Stellar Burgers — UI-тесты

Автотесты интерфейса [Stellar Burgers](https://stellarburgers.education-services.ru/):
`pytest` + `selenium` + `seletools` + `allure-pytest`

## Что проверяется

| Файл | Проверки |
|---|---|
| `tests/test_main_functionality.py` | переход в «Конструктор»; переход в «Ленту заказов»; окно деталей ингредиента;|
| `tests/test_order_feed.py` | счётчик «Выполнено за всё время»; счётчик «Выполнено за сегодня»; номер заказа в разделе «В работе» |

## Структура

- `locators/` — локаторы страниц
- `pages/` — Page Object: `BasePage`, `MainPage`, `FeedPage`
- `conftest.py` — фикстуры
- `helpers.py` — создание и удаление пользователя через API
- `data.py` — адреса и константы
- `allure_results/` — результаты прогона для Allure

## Запуск


```bash
pip install -r requirements.txt
pytest                          # оба браузера (по умолчанию --browser=all)
pytest --browser=chrome         # только Chrome
pytest --browser=firefox        # только Firefox
HEADLESS=1 pytest               # без окна браузера
```
## Отчёт Allure

```bash
allure serve allure_results
```
