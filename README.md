Проект содержит UI- и API-автотесты:

- UI: тестирование магазина https://www.saucedemo.com
- API: тестирование https://www.automationexercise.com

## Технологии и инструменты

- Python
- Pytest
- Selene
- Selenium WebDriver (UI)
- Allure Report (отчётность)
- Jenkins (CI)
- Telegram notifications
- Allure TestOps
- Selenoid

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

### Подготовка окружения

Перед запуском тестов необходимо создать файл с переменными окружения `.env` в корне проекта.   
В файле `.env` заполнить данные для доступа к selenoid, веб-сайту saucedemo.   
Шаблон заполнения:

```
# Ссылка на ресурс для апи-тестирования
AUTOMATIONEXERCISE_API_URL=https://www.automationexercise.com/api 
# Триггер для локального запуска
RUN_MODE=local
# Данные для авторизации на ресурсе для UI-тестирования
SAUCEDEMO_URL=https://www.saucedemo.com
SAUCEDEMO_LOGIN=***
SAUCEDEMO_LOGIN_FAIL=***
SAUCEDEMO_PASSWORD=***
```

Далее необходимо установить зависимости: `pip install -r requirements.txt`

### Запуск тестов

- Запуск всех тестов: `pytest`
- Запуск только UI: `pytest tests/tests_UI_saucedemo`
- Запуск только API: `pytest tests/tests_API_automationexercise`
- Генерация Allure-результатов: `pytest --alluredir=allure-results --clean-alluredir`
- Просмотр Allure локально: `allure serve allure-results`

## Запуск тестов в selenoid

Для запуска тестов с помощью Jenkins в selenoid нужно:

- Перейти в существующий проект: https://jenkins.autotests.cloud/job/22_final_project_kostina/
- Запустить проект с помощью функции "Build now"

## Jenkins

Jenkins Project: **https://jenkins.autotests.cloud/job/22_final_project_kostina/**

Скриншот страницы Project:

![Скриншот страницы Jenkins Project:](/resources/jenkins_project.png)

### Allure report в Jenkins

Allure Report: **https://jenkins.autotests.cloud/job/22_final_project_kostina/allure/**

Скриншот Allure Report:

![Скриншот Allure Report](/resources/allure_report.png)

## Allure TestOps

Test cases: **https://allure.autotests.cloud/project/5050/test-cases**

Dashboards: **https://allure.autotests.cloud/project/5050/dashboards**

![Скриншот Allure TestOps](/resources/testops_dashboard.png)

## Уведомления в Telegram

Скриншот уведомления:

![Скриншот уведомления в Telegram](/resources/telegram_notification.png)
