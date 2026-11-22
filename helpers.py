import uuid

import allure
import requests

from data import Urls

TIMEOUT = 30


def generate_user():
    unique = uuid.uuid4().hex[:12]
    return {
        "email": f"test_user_{unique}@example.com",
        "password": f"Pass_{unique}",
        "name": f"User {unique[:6]}",
    }


def register_user(payload):
    with allure.step("Создать пользователя через API"):
        response = requests.post(Urls.API_REGISTER, json=payload, timeout=TIMEOUT)
        body = response.json()
        return {
            "access_token": body["accessToken"],
            "refresh_token": body["refreshToken"],
        }


def delete_user(access_token):
    with allure.step("Удалить пользователя через API"):
        response = requests.delete(
            Urls.API_USER, headers={"Authorization": access_token}, timeout=TIMEOUT
        )
        response.raise_for_status()
