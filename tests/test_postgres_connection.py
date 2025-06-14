import psycopg2
import sys

def test_connection():
    """Тестирует подключение к PostgreSQL."""
    try:
        # Пробуем подключиться к базе данных postgres
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",  # Замените на ваш пароль
            host="localhost",
            port="5432"
        )
        print("✅ Успешное подключение к PostgreSQL!")
        
        # Проверяем версию сервера
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"Версия PostgreSQL: {version[0]}")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print("❌ Ошибка подключения к PostgreSQL:")
        print(str(e))
        print("\nУбедитесь, что:")
        print("1. PostgreSQL установлен")
        print("2. Служба PostgreSQL запущена (services.msc)")
        print("3. Порт 5432 не занят другим приложением")
        print("4. Пароль указан верно")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    if not test_connection():
        sys.exit(1) 