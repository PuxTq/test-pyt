import os
import json
from playwright.sync_api import Page, TimeoutError


def get_auth_file_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'auth.json')


def load_credentials():
    auth_file_path = get_auth_file_path()

    try:
        with open(auth_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            login = data.get('login')
            password = data.get('password')
            if not login or not password:
                raise ValueError("В файле auth.json должны быть заполнены login и password")
            return login, password
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {auth_file_path} не найден")
    except json.JSONDecodeError:
        raise ValueError("Ошибка формата файла auth.json")


def close_region_popup(page: Page):
    try:
        btn_yes = page.get_by_role("link", name="Да", exact=True)
        btn_yes.wait_for(state="visible", timeout=5000)
        btn_yes.click()
    except TimeoutError:
        pass


def perform_login(page: Page):
    try:
        close_region_popup(page)

        login_trigger = page.locator(".h").filter(has_text="Войти")
        login_trigger.wait_for(state="visible")
        login_trigger.click()

        LOGIN, PASSWORD = load_credentials()

        login_field = page.get_by_role("textbox", name="Логин")
        login_field.wait_for(state="visible")
        login_field.fill(LOGIN)

        password_field = page.get_by_role("textbox", name="*****")
        password_field.wait_for(state="visible")
        password_field.fill(PASSWORD)

        submit_btn = page.get_by_role("button", name="Войти")
        submit_btn.wait_for(state="visible")
        submit_btn.click()

        profile_indicator = page.locator(
            ".user-profile, .cabinet-link, a[href*='cabinet'], span.logout, #pnlLogin:not(.guest)"
        ).first
        profile_indicator.wait_for(state="visible", timeout=20000)
        print("Авторизация прошла успешно")
        return True

    except TimeoutError as te:
        print(f"Ошибка таймаута: {te}")
        raise
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
    finally:
        print("Завершение процесса авторизации")