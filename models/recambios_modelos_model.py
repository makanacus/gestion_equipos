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

    def update(self, id_recambio, id_modelo, new_id_recambio=None, new_id_modelo=None):
        """
        Actualiza una relación existente entre un recambio y un modelo.
        
        :param id_recambio: ID del recambio actual.
        :param id_modelo: ID del modelo actual.
        :param new_id_recambio: Nuevo ID del recambio (opcional).
        :param new_id_modelo: Nuevo ID del modelo (opcional).
        :return: None
        """
        updates = []
        params = []

        if new_id_recambio is not None:
            updates.append("id_recambio=?")
            params.append(new_id_recambio)
        if new_id_modelo is not None:
            updates.append("id_modelo=?")
            params.append(new_id_modelo)

        if not updates:
            print("No se proporcionaron datos para actualizar.")
            return

        query = f"UPDATE Recambios_Modelos SET {', '.join(updates)} WHERE id_recambio=? AND id_modelo=?"
        params.extend([id_recambio, id_modelo])

        try:
            self.db.execute_query(query, tuple(params))
            print(f"Relación actualizada: Recambio '{id_recambio}' -> Modelo '{id_modelo}'.")
        except Exception as e:
            print(f"Error al actualizar la relación: {e}")

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