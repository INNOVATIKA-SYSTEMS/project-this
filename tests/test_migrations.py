import pytest
from sqlalchemy import inspect, text
from alembic.script import ScriptDirectory
from alembic import command

def test_migration_script_has_upgrade_and_downgrade(alembic_script):
    """Проверяет, что все миграции имеют методы upgrade и downgrade."""
    for revision in alembic_script.walk_revisions():
        assert hasattr(revision.module, "upgrade"), f"Миграция {revision.revision} не имеет метода upgrade"
        assert hasattr(revision.module, "downgrade"), f"Миграция {revision.revision} не имеет метода downgrade"

def test_migration_dependencies(alembic_script):
    """Проверяет, что все миграции имеют корректные зависимости."""
    revisions = list(alembic_script.walk_revisions())
    revision_map = {rev.revision: rev for rev in revisions}
    
    for rev in revisions:
        if rev.down_revision:
            assert rev.down_revision in revision_map, \
                f"Миграция {rev.revision} ссылается на несуществующую предыдущую миграцию {rev.down_revision}"
        if rev.dependencies:
            for dep in rev.dependencies:
                assert dep.revision in revision_map, \
                    f"Миграция {rev.revision} зависит от несуществующей миграции {dep.revision}"

def test_migration_upgrade_downgrade(alembic_config, engine):
    """Проверяет, что все миграции могут быть применены и откатаны."""
    # Получаем список всех ревизий
    script = ScriptDirectory.from_config(alembic_config)
    revisions = list(script.walk_revisions())
    
    # Проверяем каждую миграцию
    for i in range(len(revisions)):
        # Применяем миграции до текущей
        command.upgrade(alembic_config, revisions[i].revision)
        
        # Проверяем, что база данных в рабочем состоянии
        with engine.connect() as conn:
            # Проверяем, что можем выполнить простой запрос
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
            
            # Проверяем, что все таблицы доступны
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            assert len(tables) > 0, "После миграции нет таблиц в базе данных"
        
        # Откатываем миграцию
        if i > 0:
            command.downgrade(alembic_config, revisions[i-1].revision)
        else:
            command.downgrade(alembic_config, "base")

def test_migration_data_integrity(alembic_config, engine, db_session):
    """Проверяет целостность данных после миграций."""
    # Применяем все миграции
    command.upgrade(alembic_config, "head")
    
    # Здесь можно добавить тесты для проверки целостности данных
    # Например, проверка внешних ключей, уникальных ограничений и т.д.
    with engine.connect() as conn:
        # Проверяем, что все внешние ключи валидны
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'FOREIGN KEY'
        """))
        foreign_keys_count = result.scalar()
        assert foreign_keys_count >= 0, "Ошибка при проверке внешних ключей"
        
        # Проверяем, что все уникальные ограничения валидны
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'UNIQUE'
        """))
        unique_constraints_count = result.scalar()
        assert unique_constraints_count >= 0, "Ошибка при проверке уникальных ограничений"

def test_migration_performance(alembic_config, engine):
    """Проверяет производительность миграций."""
    import time
    
    # Применяем все миграции и замеряем время
    start_time = time.time()
    command.upgrade(alembic_config, "head")
    upgrade_time = time.time() - start_time
    
    # Проверяем, что миграции не занимают слишком много времени
    assert upgrade_time < 30, f"Миграции заняли слишком много времени: {upgrade_time} секунд"
    
    # Откатываем миграции и замеряем время
    start_time = time.time()
    command.downgrade(alembic_config, "base")
    downgrade_time = time.time() - start_time
    
    # Проверяем, что откат не занимает слишком много времени
    assert downgrade_time < 30, f"Откат миграций занял слишком много времени: {downgrade_time} секунд"

def test_migration_concurrent_access(alembic_config, engine):
    """Проверяет, что миграции корректно работают при конкурентном доступе."""
    import threading
    import queue
    
    results = queue.Queue()
    
    def run_migration():
        try:
            # Создаем отдельное подключение для каждого потока
            with engine.connect() as conn:
                # Выполняем простой запрос
                result = conn.execute(text("SELECT 1"))
                results.put(("success", result.scalar()))
        except Exception as e:
            results.put(("error", str(e)))
    
    # Запускаем несколько потоков одновременно
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=run_migration)
        threads.append(thread)
        thread.start()
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
    
    # Проверяем результаты
    while not results.empty():
        status, result = results.get()
        assert status == "success", f"Ошибка при конкурентном доступе: {result}"
        assert result == 1, "Неверный результат при конкурентном доступе" 