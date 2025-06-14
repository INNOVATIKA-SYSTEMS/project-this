import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

def create_test_database():
    """Создает тестовую базу данных, если она не существует."""
    # Параметры подключения к PostgreSQL
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    TEST_DB_NAME = "test_db"

    # Создаем подключение к базе данных postgres (системная БД)
    postgres_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    engine = create_engine(postgres_url)

    try:
        # Проверяем существование базы данных
        with engine.connect() as conn:
            result = conn.execute(text(
                f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'"
            ))
            database_exists = result.scalar() is not None

        if not database_exists:
            # Создаем базу данных
            with engine.connect() as conn:
                # Закрываем все существующие подключения к базе данных
                conn.execute(text(
                    f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
                    AND pid <> pg_backend_pid()
                    """
                ))
                # Создаем новую базу данных
                conn.execute(text(f'CREATE DATABASE {TEST_DB_NAME}'))
                print(f"База данных {TEST_DB_NAME} успешно создана")
        else:
            print(f"База данных {TEST_DB_NAME} уже существует")

        # Обновляем переменную окружения для тестов
        os.environ["TEST_DATABASE_URL"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
        print(f"TEST_DATABASE_URL установлен: {os.environ['TEST_DATABASE_URL']}")

    except ProgrammingError as e:
        print(f"Ошибка при создании базы данных: {str(e)}")
        print("\nУбедитесь, что:")
        print("1. PostgreSQL установлен и запущен")
        print("2. Пользователь имеет права на создание баз данных")
        print("3. Параметры подключения корректны")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_test_database() 