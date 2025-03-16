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

    # Ejecutar una consulta sin necesidad de preocuparnos de cerrar la conexión
    def execute_query(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                conn.commit()  # Aseguramos que se hace commit después de una inserción/actualización
            except sqlite3.Error as e:
                print(f"Error al ejecutar la consulta: {e}")
                conn.rollback()  # En caso de error, revertir la transacción

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

