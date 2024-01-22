# Инструкции по запуску проекта Ylab-test-1

1. Склонируйте репозиторий:

   ```bash
   git clone git@github.com:YudinRomanovich/Ylab-test-1.git
   
2. Перейдите в папку с проектом:
   ```bash
   cd Ylab-test-1

3. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv

4. Активируйте виртуальное окружение:
   ```bash
   source venv/bin/activate

5. Установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt

6. Запустите PostgreSQL через Docker:
   ```bash
   sudo docker run -p 5950:5432 --name test_ylab_lec1 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:13.3

7. Запустите контейнер PostgreSQL:
   ```bash
   sudo docker start test_ylab_lec1

8. Прогоните миграции Alembic:
   ```bash
   alembic upgrade head

9. Запустите приложение, перейдите в папку src и выполните следующую команду:
   ```bash
   uvicorn main:app --reload

10. Запустите тесты через Postman: сначала выполните тестовый сценарий, затем сбросьте переменные среды, после чего протестируйте API.


