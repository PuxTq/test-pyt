import allure
from playwright.sync_api import sync_playwright
from login_actions import perform_login, close_region_popup


@allure.title("Открытие сайта")
def test_site_opening():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            assert page.url == "https://www.exist.ru/", "Неверный URL главной страницы"
            assert "Exist.ru" in page.title(), "Неверное название главной страницы"
            print("Тест открытия сайта пройден")
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Регистрация")
def test_registration():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            close_region_popup(page)

            page.get_by_role("link", name="Регистрация").click()
            page.get_by_role("textbox", name="Фамилия").fill("Иванов")
            page.get_by_role("textbox", name="Имя").fill("Иван")
            page.get_by_role("textbox", name="Отчество").fill("Иванович")
            page.get_by_role("textbox", name="999-99-99").fill("9991112233")
            page.get_by_role("textbox", name="email@domain.name").fill("test_user123@mail.ru")

            reg_button = page.get_by_role("button", name="Зарегистрироваться")
            reg_button.wait_for(state="visible", timeout=20000)
            assert reg_button.is_enabled(), "Кнопка регистрации недоступна"
            print("Тест регистрации пройден")
        except Exception as e:
            print(f"Ошибка регистрации: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Авторизация")
def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            success = perform_login(page)
            assert success, "Тест авторизации не пройден"
            print("Тест авторизации пройден")
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")

@allure.title("Неправильная авторизация")
def test_login_invalid():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            close_region_popup(page)

            page.locator(".h").filter(has_text="Войти").click()
            page.get_by_role("textbox", name="Логин").fill("+70000000000")
            page.get_by_role("textbox", name="*****").fill("wrong_password_123")
            page.get_by_role("button", name="Войти").click()

            # Проверка: появилось сообщение об ошибке (локатор предположительный, нужно уточнить по сайту)
            error_message = page.locator("text=/неверн|ошибк|не найден/i").first
            error_message.wait_for(state="visible", timeout=20000)

            # Проверка: вход не выполнен - в шапке нет ссылки "Выход"
            assert page.locator("#logout").count() == 0, "Вход выполнен с неправильным логином и паролем"
            print("Тест неправильной авторизации пройден")
        except Exception as e:
            print(f"Ошибка в тесте неправильной авторизации: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")

@allure.title("Гараж: добавление ТС")
def test_garage_add_car():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            assert perform_login(page), "Не удалось выполнить авторизацию"

            page.locator("#garageFloatHead").get_by_text("Гараж").click()
            page.get_by_text("Добавить ТС").click()
            page.get_by_role("textbox").fill("Z8NBAABD0H0048425")
            page.get_by_role("button", name="Продолжить").click()
            page.get_by_role("link", name="Datsun on-Do 1.6").click()
            page.get_by_role("button", name="Сохранить").click()

            page.get_by_role("link", name="Личный кабинет").click()
            page.locator(".menu-root-node").click()
            page.locator("#garageFloatHead").get_by_text("Гараж").click()

            car_link = page.get_by_role("link", name="Datsun on-Do").first
            car_link.wait_for(state="visible", timeout=20000)
            car_name = car_link.inner_text()
            assert "Datsun on-Do" in car_name, f"Неверное название машины: {car_name}"
            car_link.click()
            print("Тест добавления ТС пройден")
        except Exception as e:
            print(f"Ошибка добавления ТС: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Проверка запрошенного артикула")
def test_requested_article():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            assert perform_login(page), "Не удалось выполнить авторизацию"

            page.locator("#garageFloatHead").get_by_text("Гараж").click()
            page.get_by_text("Datsun on-Do").click()
            page.locator("#originalLiMain").get_by_role("link", name="Оригинальный каталог Datsun").click()
            page.get_by_text("ДВИГАТЕЛЬ").click()
            page.get_by_role("link", name="Блок цилиндров и поддон картера; ASSEMBLY image 110A").click()
            with page.expect_popup() as page1_info:
                page.get_by_role("link", name="Цены").first.click()
            page1 = page1_info.value
            page1.get_by_role("link", name="Datsun   110105PA0A").click()
            print("Тест запрошенного артикула пройден")
        except Exception as e:
            print(f"Ошибка проверки артикула: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Гараж: удаление ТС")
def test_garage_remove_car():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            assert perform_login(page), "Не удалось выполнить авторизацию"

            page.locator("#garageFloatHead").get_by_text("Гараж").click()
            car_card = page.locator(".car-info--garage-menu").filter(has_text="Z8NBAABD0H0048425").first
            car_card.wait_for(state="visible", timeout=2000)
            car_card.click()
            page.locator("#phCarInfo").get_by_role("link", name="Datsun on-Do").click()

            delete_link = page.get_by_role("link", name="Удалить")
            delete_link.wait_for(state="visible", timeout=2000)
            delete_link.click()

            confirm_btn = page.locator("#confirmRemoveOK")
            confirm_btn.wait_for(state="visible", timeout=2000)
            confirm_btn.click()
            confirm_btn.wait_for(state="hidden", timeout=2000)

            page.goto("https://www.exist.ru/")
            close_region_popup(page)
            page.locator("#garageFloatHead").get_by_text("Гараж").click()
            page.wait_for_timeout(200)

            car_name = page.locator(".car-info--garage-menu .car-info__car-name").filter(has_text="Datsun on-Do")
            assert car_name.count() == 0, "Машина осталась в гараже после удаления"
            print("Машины в гараже нет, тест удаления ТС пройден")
        except Exception as e:
            print(f"Ошибка удаления ТС: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")

@allure.title("Каталог по маслу")
def test_catalog_by_oil():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            close_region_popup(page)
            page.get_by_role("link", name="Каталоги", exact=True).click()
            page.get_by_role("link", name="Масла моторные").click()
            page.get_by_role("img", name="Lukoil 3149902").click()

            result_indicator = page.locator(".wrap, .descr, .ucatprcdiv").first
            result_indicator.wait_for(state="visible", timeout=20000)
            assert result_indicator.is_visible(), "Масло не найдено"
            print("Масло найдено, тест каталога по маслу пройден")
        except Exception as e:
            print(f"Ошибка каталога по маслу: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Поиск масла")
def test_oil_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            close_region_popup(page)

            page.locator("#pcode").fill("GENESIS ARMORTECH 5W-40")
            page.get_by_role("button", name="Найти").click()

            page.get_by_role("link", name="• 5W-").click()

            page.locator("p", has_text="Lukoil 3148675").first.click()

            page.wait_for_load_state()

            result_indicator = page.locator(".descr, .ucatprcdiv, .price").first
            result_indicator.wait_for(state="visible", timeout=20000)
            assert result_indicator.is_visible(), "Масло не найдено"
            print("Масло найдено, тест поиска масла пройден")
        except Exception as e:
            print(f"Ошибка поиска масла: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Поиск по VIN")
def test_vin_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            close_region_popup(page)

            page.locator("#pcode").fill("Z8NBAABD0H0048425")
            page.get_by_role("button", name="Найти").click()

            page.locator("#imgCar").click()
            page.get_by_role("heading", name="Datsun on-Do").click()
            page.get_by_role("link", name="Масла и жидкости").click()
            page.get_by_role("link", name="Liqui Moly Top Tec 4200 5W-30").click()

            result_indicator = page.locator(".fluid-goods-block, .oil-description").first
            result_indicator.wait_for(state="visible", timeout=20000)
            assert result_indicator.is_visible(), "Масло не найдено"
            print("Масло найдено, тест поиска по VIN пройден")
        except Exception as e:
            print(f"Ошибка поиска по VIN: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Навигация по каталогу (BMW)")
def test_catalog_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://www.exist.ru/")
            close_region_popup(page)

            page.get_by_role("link", name="BMW").click()
            page.get_by_role("link", name="X1 China III").click()
            page.get_by_role("link", name="sDrive20Li").click()
            page.get_by_role("link", name="Оригинальный каталог Ссылка на внешний сайт").click()
            page.get_by_role("radio", name="Россия").check()
            page.get_by_role("link", name="' E46 Седан").click()
            page.get_by_role("link", name="318i N42").click()
            page.get_by_role("link", name="2002").click()
            page.get_by_role("link", name="ЯНВАРЬ").click()
            page.get_by_role("link", name="ДВИГАТЕЛЬ", exact=True).click()
            page.get_by_role("link", name="ВЫПУСКНОЙ КОЛЛЕКТОР").click()
            page.get_by_role("link", name="Подгруппа 1 из").click()

            with page.expect_popup() as page1_info:
                page.get_by_role("link", name="Цена").first.click()
            page1 = page1_info.value
            page1.wait_for_load_state()

            print("Тест навигации пройден")
        except Exception as e:
            print(f"Ошибка навигации: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")


@allure.title("Проверка добавления в корзину и удаления")
def test_order_submission():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        try:
            # 1. Открытие сайта и авторизация
            page.goto("https://www.exist.ru/")
            assert perform_login(page), "Не удалось выполнить авторизацию"

            # 2. Поиск
            page.locator("#pcode").click()
            page.locator("#pcode").fill("GENESIS ARMORTECH 5W-40")
            page.get_by_role("button", name="Найти").click()

            # 3. Выбор фильтра и товара
            page.get_by_role("link", name="• 25W-").click()
            page.locator("p", has_text="Liqui Moly 25026").first.click()

            # 4. РАБОТА С IFRAME: Добавление в корзину
            iframe = page.frame_locator("iframe[name^='fancybox-frame']")
            add_btn = iframe.locator("a.basket[title='Добавить в корзину']").first
            add_btn.wait_for(state="visible", timeout=20000)
            add_btn.click()

            # 5. Закрываем всплывающее окно и ждем его исчезновения
            close_btn = page.locator("#fancybox-close")
            close_btn.wait_for(state="visible", timeout=10000)
            close_btn.click(force=True)
            close_btn.wait_for(state="hidden", timeout=10000)

            # 6. Переходим в корзину и удаляем товар
            page.get_by_role("link", name="Корзина").first.click()

            remove_btn = page.get_by_role("link", name="Удалить из корзины").first
            remove_btn.wait_for(state="visible", timeout=20000)
            remove_btn.click()

            print("Тест корзины пройден")
        except Exception as e:
            print(f"Ошибка в тесте корзины: {e}")
            raise
        finally:
            browser.close()
            print("Браузер закрыт")