from database import Database

class RecambiosModelosModel:
    def __init__(self):
        self.db = Database()

    def create(self, id_recambio, id_modelo):
        """
        Crea una nueva relación entre un recambio y un modelo.
        
        :param id_recambio: ID del recambio.
        :param id_modelo: ID del modelo.
        :return: None
        """
        query = """INSERT INTO Recambios_Modelos (id_recambio, id_modelo)
                   VALUES (?, ?)"""
        try:
            result = self.db.execute_query(query, (id_recambio, id_modelo))
            print(f"Relación creada: Recambio '{id_recambio}' -> Modelo '{id_modelo}'.")
            return result
        except Exception as e:
            print(f"Error al crear la relación: {e}")

    def get_all(self):
        """
        Obtiene todas las relaciones entre recambios y modelos.
        
        :return: Lista de diccionarios con la información de las relaciones.
        """
        query = "SELECT * FROM Recambios_Modelos"
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener las relaciones: {e}")
            return []

    def get_by_recambio(self, id_recambio):
        """
        Obtiene todas las relaciones asociadas a un recambio específico.
        
        :param id_recambio: ID del recambio.
        :return: Lista de diccionarios con la información de las relaciones.
        """
        query = "SELECT * FROM Recambios_Modelos WHERE id_recambio=?"
        try:
            return self.db.fetch_query(query, (id_recambio,))
        except Exception as e:
            print(f"Error al obtener las relaciones por recambio: {e}")
            return []

    def get_by_modelo(self, id_modelo):
        """
        Obtiene todas las relaciones asociadas a un modelo específico.
        
        :param id_modelo: ID del modelo.
        :return: Lista de diccionarios con la información de las relaciones.
        """
        query = "SELECT * FROM Recambios_Modelos WHERE id_modelo=?"
        try:
            return self.db.fetch_query(query, (id_modelo,))
        except Exception as e:
            print(f"Error al obtener las relaciones por modelo: {e}")
            return []

    def update_relaciones_by_recambio(self, id_recambio, nuevos_modelos):
        """
        Actualiza las relaciones de un recambio con los modelos.
        
        :param id_recambio: ID del recambio a actualizar.
        :param nuevos_modelos: Lista de IDs de modelos seleccionados.
        :return: True si se actualizó correctamente, False en caso de error.
        """
        try:
            # 1️⃣ Eliminar todas las relaciones antiguas
            delete_query = "DELETE FROM Recambios_Modelos WHERE id_recambio=?"
            self.db.execute_query(delete_query, (id_recambio,))

            # 2️⃣ Insertar las nuevas relaciones
            insert_query = "INSERT INTO Recambios_Modelos (id_recambio, id_modelo) VALUES (?, ?)"
            for id_modelo in nuevos_modelos:
                self.db.execute_query(insert_query, (id_recambio, id_modelo))

            print(f"Relaciones actualizadas para recambio {id_recambio}: {nuevos_modelos}")
            return True

        except Exception as e:
            print(f"Error al actualizar relaciones: {e}")
            return False

    def delete(self, id_recambio, id_modelo):
        """
        Elimina una relación entre un recambio y un modelo.
        
        :param id_recambio: ID del recambio.
        :param id_modelo: ID del modelo.
        :return: None
        """
        query = "DELETE FROM Recambios_Modelos WHERE id_recambio=? AND id_modelo=?"
        try:
            self.db.execute_query(query, (id_recambio, id_modelo))
            print(f"Relación eliminada: Recambio '{id_recambio}' -> Modelo '{id_modelo}'.")
        except Exception as e:
            print(f"Error al eliminar la relación: {e}")