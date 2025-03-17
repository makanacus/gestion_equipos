from database import Database

class RecambioModel:
    def __init__(self):
        self.db = Database()

    def create(self, recambio, cantidad, cantidad_minima):
        query = """INSERT INTO Recambios (recambio, cantidad, cantidad_minima)
                VALUES (?, ?, ?)"""
        try:
            cursor = self.db.execute_query(query, (recambio, cantidad, cantidad_minima))  # ✅ Guardar cursor ultimo id
            
            if cursor is None:
                raise Exception("Error al ejecutar la consulta de inserción.")

            recambio_id = cursor
            
            if recambio_id is None:  # ⚠️ Evita `if not recambio_id` porque 0 es válido
                raise Exception("Error al obtener el ID del nuevo recambio.")

            print(f"✅ Recambio '{recambio}' creado correctamente con ID {recambio_id}.")
            return recambio_id
        except Exception as e:
            print(f"❌ Error al crear el recambio: {e}")
            return None



    def update(self, recambio_id, recambio=None, cantidad=None, cantidad_minima=None):
        """
        Actualiza la información de un recambio existente.
        
        :param recambio_id: ID del recambio a actualizar.
        :param recambio: Nuevo nombre del recambio (opcional).
        :param cantidad: Nueva cantidad disponible (opcional).
        :param cantidad_minima: Nueva cantidad mínima de stock (opcional).
        :return: True si se actualizó correctamente, False en caso de error.
        """
        updates = []
        params = []

        if recambio is not None:
            updates.append("recambio=?")
            params.append(recambio)
        if cantidad is not None:
            updates.append("cantidad=?")
            params.append(cantidad)
        if cantidad_minima is not None:
            updates.append("cantidad_minima=?")
            params.append(cantidad_minima)

        # Si se actualiza cantidad o cantidad_minima, recalculamos stock_bajo
        if cantidad is not None or cantidad_minima is not None:
            updates.append("stock_bajo=?")
            params.append(cantidad < cantidad_minima)

        if not updates:
            print("No se proporcionaron datos para actualizar.")
            return False

        query = f"UPDATE Recambios SET {', '.join(updates)} WHERE id=?"
        params.append(recambio_id)

        try:
            self.db.execute_query(query, tuple(params))
            print(f"Recambio con ID '{recambio_id}' actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar el recambio: {e}")
            return False

    def delete(self, recambio_id):
        """
        Elimina un recambio de la base de datos.
        
        :param recambio_id: ID del recambio a eliminar.
        :return: True si se eliminó correctamente, False en caso de error.
        """
        query = "DELETE FROM Recambios WHERE id=?"
        try:
            self.db.execute_query(query, (recambio_id,))
            print(f"Recambio con ID '{recambio_id}' eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar el recambio: {e}")
            return False

    def get_by_id(self, recambio_id):
        """
        Obtiene un recambio por su ID.
        
        :param recambio_id: ID del recambio.
        :return: Diccionario con la información del recambio o None si no se encuentra.
        """
        query = "SELECT id, recambio, cantidad, cantidad_minima, stock_bajo FROM Recambios WHERE id=?"
        try:
            result = self.db.fetch_query(query, (recambio_id,))
            if result:
                recambio_data = result[0]
                return {
                    "id": recambio_data[0],
                    "recambio": recambio_data[1],
                    "cantidad": recambio_data[2],
                    "cantidad_minima": recambio_data[3],
                    "stock_bajo": bool(recambio_data[4])
                }
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
        query = "SELECT id, recambio, cantidad, cantidad_minima, stock_bajo FROM Recambios"
        try:
            results = self.db.fetch_query(query)
            return [
                {
                    "id": row[0],
                    "recambio": row[1],
                    "cantidad": row[2],
                    "cantidad_minima": row[3],
                    "stock_bajo": bool(row[4])
                }
                for row in results
            ]
        except Exception as e:
            print(f"Error al obtener los recambios: {e}")
            return []

    def get_by_recambio(self, recambio):
        """
        Obtiene todos los recambios cuyo nombre contenga la cadena ingresada.
        
        :param recambio: Parte del nombre del recambio a buscar.
        :return: Lista de diccionarios con la información de los recambios.
        """
        query = "SELECT id, recambio, cantidad, cantidad_minima, stock_bajo FROM Recambios WHERE recambio LIKE ?"
        try:
            results = self.db.fetch_query(query, (f"%{recambio}%",))
            return [
                {
                    "id": row[0],
                    "recambio": row[1],
                    "cantidad": row[2],
                    "cantidad_minima": row[3],
                    "stock_bajo": bool(row[4])
                }
                for row in results
            ]
        except Exception as e:
            print(f"Error al obtener los recambios por nombre: {e}")
            return []
