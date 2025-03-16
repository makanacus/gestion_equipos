from database import Database

class RecambioModel:
    def __init__(self):
        self.db = Database()

    def create(self, modelo_equipo, recambio, cantidad, cantidad_minima):
        """
        Crea un nuevo recambio en la base de datos.
        
        :param modelo_equipo: Lista de modelos a los que sirve el recambio (en formato JSON o texto).
        :param recambio: Nombre de la recambio o repuesto.
        :param cantidad: Cantidad disponible del recambio.
        :param cantidad_minima: Cantidad mínima de stock para el recambio.
        :return: None
        """
        query = """INSERT INTO Recambios (modelo_equipo, recambio, cantidad, cantidad_minima)
                   VALUES (?, ?, ?, ?)"""
        try:
            self.db.execute_query(query, (modelo_equipo, recambio, cantidad, cantidad_minima))
            print(f"Recambio '{recambio}' creado correctamente.")
        except Exception as e:
            print(f"Error al crear el recambio: {e}")

    def update(self, recambio_id, modelo_equipo=None, recambio=None, cantidad=None, cantidad_minima=None):
        """
        Actualiza la información de un recambio existente.
        
        :param recambio_id: ID del recambio a actualizar.
        :param modelo_equipo: Nueva lista de modelos (opcional).
        :param recambio: Nuevo nombre de la recambio (opcional).
        :param cantidad: Nueva cantidad disponible (opcional).
        :param cantidad_minima: Nueva cantidad mínima de stock (opcional).
        :return: None
        """
        updates = []
        params = []

        if modelo_equipo is not None:
            updates.append("modelo_equipo=?")
            params.append(modelo_equipo)
        if recambio is not None:
            updates.append("recambio=?")
            params.append(recambio)
        if cantidad is not None:
            updates.append("cantidad=?")
            params.append(cantidad)
        if cantidad_minima is not None:
            updates.append("cantidad_minima=?")
            params.append(cantidad_minima)

        if not updates:
            print("No se proporcionaron datos para actualizar.")
            return

        query = f"UPDATE Recambios SET {', '.join(updates)} WHERE id=?"
        params.append(recambio_id)

        try:
            self.db.execute_query(query, tuple(params))
            print(f"Recambio con ID '{recambio_id}' actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar el recambio: {e}")

    def delete(self, recambio_id):
        """
        Elimina un recambio de la base de datos.
        
        :param recambio_id: ID del recambio a eliminar.
        :return: None
        """
        query = "DELETE FROM Recambios WHERE id=?"
        try:
            self.db.execute_query(query, (recambio_id,))
            print(f"Recambio con ID '{recambio_id}' eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar el recambio: {e}")

    def get_by_id(self, recambio_id):
        """
        Obtiene un recambio por su ID.
        
        :param recambio_id: ID del recambio.
        :return: Diccionario con la información del recambio o None si no se encuentra.
        """
        query = "SELECT * FROM Recambios WHERE id=?"
        try:
            result = self.db.fetch_query(query, (recambio_id,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró el recambio con ID '{recambio_id}'.")
                return None
        except Exception as e:
            print(f"Error al obtener el recambio: {e}")
            return None

    def get_all(self):
        """
        Obtiene todos los recambios de la base de datos.
        
        :return: Lista de diccionarios con la información de los recambios.
        """
        query = "SELECT * FROM Recambios"
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener los recambios: {e}")
            return []

    def get_by_recambio(self, recambio):
        """
        Obtiene todos los recambios que coinciden con el nombre de la recambio.
        
        :param recambio: Nombre de la recambio a buscar.
        :return: Lista de diccionarios con la información de los recambios.
        """
        query = "SELECT * FROM Recambios WHERE recambio=?"
        try:
            return self.db.fetch_query(query, (recambio,))
        except Exception as e:
            print(f"Error al obtener los recambios por recambio: {e}")
            return []