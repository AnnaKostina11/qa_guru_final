Проект объединяет UI- и API-автотесты:

- UI: тестирование магазина https://www.saucedemo.com
- API: тестирование https://www.automationexercise.com

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
Перед запуском тестов необходимо создать файл с переменными окружения `.env` в корне проекта.   
В файле `.env` заполнить данные для доступа к selenoid, веб-сайту saucedemo.   
Пример заполнения:
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
Далее необходимо открыть консоль (сочетание клавиш alt+F12) и выполнить следующие шаги:
- Установить зависимости: `pip install -r requirements.txt`
- Запуск всех тестов: `pytest`
- Запуск только UI: `pytest tests/tests_UI_saucedemo`
- Запуск только API: `pytest tests/tests_API_automationexercise`
- Генерация Allure-результатов: `pytest --alluredir=allure-results --clean-alluredir`
- Просмотр Allure локально: `allure serve allure-results`

## Запуск тестов в selenoid
Для запуска тестов с помощью Jenkins в selenoid нужно настроить проект Jenkins:
- Во вкладке General:
   - `Restrict where this project can be run` - назначить лейбл "Python"
   - `Source Code Management` - указать ссылку на проект Git
- Вкладка Environment
   - `Delete workspace before build starts` - установить в "Advanced"
   - `Allure: upload results`
      - `Server` выбрать "Allure-server"
      - `Project` выбрать имя проекта
      - `Launch name` Установить значение `${JOB_NAME} - #${BUILD_NUMBER}`
      - `Results` заполнить "allure-results"
- Вкладка Build Steps
   - Создать текстовый файл с именем ".env", заполнить, установить чек-бокс "Overwrite file" и "Create at Workspace":
    ```
    # Ссылка на ресурс для апи-тестирования
    AUTOMATIONEXERCISE_API_URL=https://www.automationexercise.com/api 
    # Триггер для запуска через selenoid
    RUN_MODE=remote
    # Данные selenoid
    SELENOID_LOGIN=***
    SELENOID_PASS=***
    SELENOID_URL=selenoid.autotests.cloud/wd/hub
    # Данные для авторизации на ресурсе для UI-тестирования
    SAUCEDEMO_URL=https://www.saucedemo.com
    SAUCEDEMO_LOGIN=***
    SAUCEDEMO_LOGIN_FAIL=***
    SAUCEDEMO_PASSWORD=***
    ```
   - Создать текстовый файл с именем "notifications/config.json", заполнить, установить чек-бокс "Overwrite file" и "Create at Workspace":
   ```
    {
      "base": {
        "project": "${JOB_BASE_NAME}",
        "environment": "Prod",
        "comment": "Jenkins complete tests",
        "reportLink": "${BUILD_URL}",
        "language": "en",
        "allureFolder": "allure-report",
        "enableChart": true
      },
      "telegram": {
        "token": "8582183300:AAEgYztF2cHX4I05WHb4XG6T4dLBGOB3tpE",
        "chat": "-1003298690377",
        "replyTo": ""
      }
    }
    ```
   - Создать скрипт "Execute shell", заполнить:
   ```
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # Allure results
    pytest --alluredir=allure-results --clean-alluredir .
    ```
- Вкладка Post-build Actions
   - Добавить "Allure Report", указать на директорию "allure-results"
   - Через оператор "AND" добавить скрипт в "Post build task", заполнить:
   ```
    cd ..
    FILE=allure-notifications-4.11.0.jar
    if [ ! -f "$FILE" ]; then
       wget https://github.com/qa-guru/allure-notifications/releases/download/4.11.0/allure-notifications-4.11.0.jar
    fi
    ```
   - Через оператор "AND" добавить еще один скрипт:
   ```
    java "-DconfigFile=notifications/config.json" -jar ../allure-notifications-4.11.0.jar
    ```
- Сохранить
- Запустить с помощью функции "Build now"
## CI: Jenkins

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
