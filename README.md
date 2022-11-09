# Проектная работа 10 спринта, когорта 18, команда #8

https://github.com/cmrd-a/notifications_sprint_1

## Проект "Фильмотека"
Состоит из:
 - ETL. Перегоняет данные из PostgreSQL в ElasticSearch.
 - Админка для создания, изменения и удаления вышеобозначенных объектов.
 - API для поиска информации о фильмах, жанрах и актёрах.
 - Сервис авторизации. Позволяет пользователю создать и пользоваться своей учётной записью, администратору - управлять правами пользователей.

### Запуск сервисов:
 1. `cp .env.example .env`
 2. `cp auth.env.example auth.env`
 3. `make prod_up`

API доступно по адресу: http://localhost/api/docs.

А админка по http://localhost/admin/. Логин и пароль 'admin'.

### Запуск тестов:
 1. `cp tests/functional/.env.example tests/functional/.env`
 2. `make tests_up`

### Генерация клиента Auth:
 1. `make prod_up`
 2. `curl localhost/auth/openapi.yaml -o auth_openapi.yaml`
 3. `docker run --rm -v $PWD:/local openapitools/openapi-generator-cli generate -i /local/auth_openapi.yaml -g python -o /local/fastapi_app/src/auth_client --skip-validate-spec --additional-properties=packageName=auth_client`
 4. `cd fastapi_app/src/auth_client`
 5. `python setup.py install`

# Auth. Система авторизации

http://localhost/auth/docs

# Analytics
 - `cp -R analytics_etl/data_example analytics_etl/data`
 - `make analyticts_up`

Confluent - http://localhost:9021
Manual config -> Address: `http://elasticlogs:9200`

### Команды для разработки:
 - `make dev_up` - поднять только БД с открытыми портами.
 - `make black` - форматировать код

---
@cmrd-a - тимлид

@nu-kotov - разработчик