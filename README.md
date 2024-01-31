# Инструкции по запуску проекта ylab-app

## Запуск приложения:

1. Склонируйте репозиторий:
    ```bash
    git clone git@github.com:YudinRomanovich/ylab_app.git
    ```

2. Перейдите в папку с проектом:
    ```bash
    cd ylab_app
    ```

3. Запустите docker compose:
    ```bash
    sudo docker-compose up -d
    ```

4. Swagger доступен на порте 9999, поэтому для доступа в браузере введите http://localhost:8000/docs

5. Остановка контейнеров:
    ```bash
    sudo docker-compose down
    ```

## Запуск тестов:

1. Остановите контейнеры с приложением:
    ```bash
    sudo docker-compose down
    ```

2. Перейдите в папку tests:
    ```bash
    cd tests
    ```

3. Запустите docker compose:
    ```bash
    sudo docker-compose up
    ```

4. Для остановки контейнеров с тестами:
    ```bash
    sudo docker-compose down
    ```

