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

1) Установить зависимости:
pip install -r requirements.txt

text

2) Запуск всех тестов:
pytest -v

text

3) Запуск только UI:
pytest -v tests/tests_UI_saucedemo

text

4) Запуск только API:
pytest -v tests/tests_API_automationexercise

text

5) Генерация Allure-результатов:
pytest --alluredir=allure-results --clean-alluredir

text

6) Просмотр Allure локально:
allure serve allure-results

text

## CI: Jenkins

- Jenkins Job: **TODO: вставить ссылку на Job**
  - 
- Скриншот страницы Job:
  - `resources/jenkins_job.png`
  

### Allure report в Jenkins
- Allure Report (build artifact / link): **TODO: вставить ссылку на Allure Report в Jenkins**
  - 
- Скриншот Allure Report:
  - `resources/allure_report.png`
  -

## Allure TestOps (опционально)

- Allure TestOps Project: **TODO: вставить ссылку**
- Launch / Test Run: **TODO: вставить ссылку на прогон**

## Уведомления в Telegram (опционально)

- Скриншот уведомления:
  - `resources/telegram_notification.png`
  
## Дополнительно

- Конфигурация окружения выполняется через переменные окружения (`.env`).
- UI тесты поддерживают локальный запуск и запуск в удалённом браузере (Selenoid) при наличии настроек.