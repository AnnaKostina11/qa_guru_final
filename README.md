Проект объединяет UI- и API-автотесты:

- UI: тестирование магазина https://www.saucedemo.com
- API: тестирование https://www.automationexercise.com


- Конфигурация окружения выполняется через переменные окружения (`.env`).
- UI тесты поддерживают локальный запуск и запуск в удалённом браузере (Selenoid).

## Технологии и инструменты

- Python
- Pytest
- Selene + Selenium WebDriver (UI)
- Requests (API)
- Allure Report (отчётность)
- Jenkins (CI)
- Telegram notifications
- Allure TestOps

## Покрытый функционал

### UI (SauceDemo)

- Авторизация:
    - стандартный пользователь
    - заблокированный пользователь
- Работа с корзиной:
    - добавление товаров в корзину
    - удаление товара из корзины
- Оформление заказа (checkout)
- Logout
- Сортировка товаров

### API (AutomationExercise)

- Создание аккаунта (POST create account)
- Проверка логина (POST verify login)
- Получение списка брендов (GET brands list)
- Обновление пользователя (PUT update account)
- Удаление аккаунта (DELETE delete account)

## Запуск тестов локально

1) Установить зависимости:
   pip install -r requirements.txt

2) Запуск всех тестов:
   pytest

3) Запуск только UI:
   pytest tests/tests_UI_saucedemo

4) Запуск только API:
   pytest tests/tests_API_automationexercise

5) Генерация Allure-результатов:
   pytest --alluredir=allure-results --clean-alluredir

6) Просмотр Allure локально:
   allure serve allure-results

## CI: Jenkins

Jenkins Job: **https://jenkins.autotests.cloud/job/22_final_project_kostina/**

Скриншот страницы Job:

![Скриншот страницы Jenkins Job:](/resources/jenkins_job.png)

### Allure report в Jenkins

Allure Report: **https://jenkins.autotests.cloud/job/22_final_project_kostina/allure/**

Скриншот Allure Report:

![Скриншот Allure Report](/resources/allure_report.png)

## Allure TestOps

- Test cases: **https://allure.autotests.cloud/project/5050/test-cases**
- Dashboards: **https://allure.autotests.cloud/project/5050/dashboards**

## Уведомления в Telegram

Скриншот уведомления:

![Скриншот уведомления в Telegram](/resources/telegram_notification.png)
