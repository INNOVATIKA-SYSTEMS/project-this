import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory

# Настройка тестовой базы данных
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost/test_db"
)

@pytest.fixture(scope="session")
def engine():
    """Создает тестовый движок базы данных."""
    engine = create_engine(TEST_DATABASE_URL)
    return engine

@pytest.fixture(scope="session")
def alembic_config():
    """Создает конфигурацию Alembic для тестов."""
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    return config

@pytest.fixture(scope="session")
def alembic_script():
    """Получает доступ к скриптам миграций."""
    return ScriptDirectory.from_config(alembic_config())

@pytest.fixture(scope="function")
def db_session(engine):
    """Создает новую сессию базы данных для каждого теста."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def migrated_db(alembic_config, engine):
    """Применяет все миграции к тестовой базе данных."""
    # Очистка базы данных перед тестами
    command.downgrade(alembic_config, "base")
    # Применение всех миграций
    command.upgrade(alembic_config, "head")
    
    yield engine
    
    # Очистка после тестов
    command.downgrade(alembic_config, "base")
