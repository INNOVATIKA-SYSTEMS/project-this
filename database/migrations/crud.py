# database/crud.py

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, Dict, Optional, List


class PostgresCRUD:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def _connect(self):
        conn = psycopg2.connect(self.dsn)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cursor

    def create(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"

        try:
            conn, cursor = self._connect()
            cursor.execute(query, values)
            new_id = cursor.fetchone()['id']
            conn.commit()
            cursor.close()
            conn.close()
            return new_id
        except Exception as e:
            print(f"[CREATE] Error: {e}")
            return None

    def read(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        where_clause = ""
        values = []

        if filters:
            clauses = [f"{key} = %s" for key in filters]
            where_clause = "WHERE " + " AND ".join(clauses)
            values = list(filters.values())

        query = f"SELECT * FROM {table} {where_clause}"

        try:
            conn, cursor = self._connect()
            cursor.execute(query, values)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"[READ] Error: {e}")
            return []

    def update(self, table: str, data: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        set_clause = ', '.join([f"{key} = %s" for key in data])
        where_clause = ' AND '.join([f"{key} = %s" for key in filters])
        values = list(data.values()) + list(filters.values())

        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        try:
            conn, cursor = self._connect()
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[UPDATE] Error: {e}")
            return False

    def delete(self, table: str, filters: Dict[str, Any]) -> bool:
        where_clause = ' AND '.join([f"{key} = %s" for key in filters])
        values = list(filters.values())

        query = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            conn, cursor = self._connect()
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[DELETE] Error: {e}")
            return False

