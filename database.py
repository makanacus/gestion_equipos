import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name="mantenimiento.db"):
        self.db_name = db_name

    # Usamos un context manager para manejar la conexión de manera más segura
    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                conn.commit()  # ✅ Confirmar cambios

                # ✅ Si la consulta fue una inserción, devolver el ID insertado
                if query.strip().lower().startswith("insert"):
                    return cursor.lastrowid  
                return True  # ✅ Para otras consultas, devolver None
            except sqlite3.Error as e:
                print(f"Error al ejecutar la consulta: {e}")
                conn.rollback()  # ❌ Revertir si hay error
                return None  # ❌ Retornar None si falla

    # Obtener resultados de una consulta
    def fetch_query(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error al ejecutar la consulta: {e}")
                return []

