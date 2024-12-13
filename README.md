# eMobileTest
## Инструкция по запуску
1) Создать `.env` файл на основе шаблона `.env_example`
2) Запустить <strong>docker-compose</strong> командой `docker-compose up --build`
3) Запустить тесты `docker-compose exec app pytest`
4) Применить миграции Alembic `docker-compose exec app alembic upgrade head`