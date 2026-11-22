import os

BASE_URL = os.getenv("STELLAR_BURGERS_URL", "https://stellarburgers.education-services.ru").rstrip("/")


class Urls:
    MAIN = f"{BASE_URL}/"
    FEED = f"{BASE_URL}/feed"
    API_REGISTER = f"{BASE_URL}/api/auth/register"
    API_USER = f"{BASE_URL}/api/auth/user"


ACTIVE_LINK_CLASS = "link_active"

ORDER_NUMBER_PLACEHOLDER = "9999"
