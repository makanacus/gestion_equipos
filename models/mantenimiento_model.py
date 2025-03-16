from database import Database

class MantenimientoModel:
    def __init__(self):
        self.db = Database()

    def create(self, equipo_id, fecha_mantenimiento, intervalo_mantenimiento, recambios_utilizados, descripcion):
        """
        Crea un nuevo mantenimiento en la base de datos.
        
        :param equipo_id: ID del equipo al que se le realiza el mantenimiento.
        :param fecha_mantenimiento: Fecha en que se realiza el mantenimiento.
        :param intervalo_mantenimiento: Intervalo en meses para el próximo mantenimiento.
        :param recambios_utilizados: Lista de recambios utilizados (puede ser NULL).
        :param descripcion: Descripción del mantenimiento (no puede ser NULL).
        :return: None
        """
        query = """INSERT INTO Mantenimientos (equipo_id, fecha_mantenimiento, intervalo_mantenimiento, recambios_utilizados, descripcion)
                   VALUES (?, ?, ?, ?, ?)"""
        try:
            self.db.execute_query(query, (equipo_id, fecha_mantenimiento, intervalo_mantenimiento, recambios_utilizados, descripcion))
            print(f"Mantenimiento para el equipo '{equipo_id}' creado correctamente.")
        except Exception as e:
            print(f"Error al crear el mantenimiento: {e}")

    def update(self, mantenimiento_id, fecha_mantenimiento=None, intervalo_mantenimiento=None, recambios_utilizados=None, descripcion=None):
        """
        Actualiza la información de un mantenimiento existente.
        
        :param mantenimiento_id: ID del mantenimiento a actualizar.
        :param fecha_mantenimiento: Nueva fecha de mantenimiento (opcional).
        :param intervalo_mantenimiento: Nuevo intervalo de mantenimiento (opcional).
        :param recambios_utilizados: Nueva lista de recambios utilizados (opcional).
        :param descripcion: Nueva descripción del mantenimiento (opcional).
        :return: None
        """
        updates = []
        params = []

        if fecha_mantenimiento is not None:
            updates.append("fecha_mantenimiento=?")
            params.append(fecha_mantenimiento)
        if intervalo_mantenimiento is not None:
            updates.append("intervalo_mantenimiento=?")
            params.append(intervalo_mantenimiento)
        if recambios_utilizados is not None:
            updates.append("recambios_utilizados=?")
            params.append(recambios_utilizados)
        if descripcion is not None:
            updates.append("descripcion=?")
            params.append(descripcion)

        if not updates:
            print("No se proporcionaron datos para actualizar.")
            return

        query = f"UPDATE Mantenimientos SET {', '.join(updates)} WHERE id=?"
        params.append(mantenimiento_id)

        try:
            self.db.execute_query(query, tuple(params))
            print(f"Mantenimiento con ID '{mantenimiento_id}' actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar el mantenimiento: {e}")

    def delete(self, mantenimiento_id):
        """
        Elimina un mantenimiento de la base de datos.
        
        :param mantenimiento_id: ID del mantenimiento a eliminar.
        :return: None
        """
        query = "DELETE FROM Mantenimientos WHERE id=?"
        try:
            self.db.execute_query(query, (mantenimiento_id,))
            print(f"Mantenimiento con ID '{mantenimiento_id}' eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar el mantenimiento: {e}")

    def get_by_id(self, mantenimiento_id):
        """
        Obtiene un mantenimiento por su ID.
        
        :param mantenimiento_id: ID del mantenimiento.
        :return: Diccionario con la información del mantenimiento o None si no se encuentra.
        """
        query = "SELECT * FROM Mantenimientos WHERE id=?"
        try:
            result = self.db.fetch_query(query, (mantenimiento_id,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró el mantenimiento con ID '{mantenimiento_id}'.")
                return None
        except Exception as e:
            print(f"Error al obtener el mantenimiento: {e}")
            return None

    def get_all(self):
        """
        Obtiene todos los mantenimientos de la base de datos.
        
        :return: Lista de diccionarios con la información de los mantenimientos.
        """
        query = "SELECT * FROM Mantenimientos"
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener los mantenimientos: {e}")
            return []

    def get_by_equipo(self, equipo_id):
        """
        Obtiene todos los mantenimientos asociados a un equipo.
        
        :param equipo_id: ID del equipo.
        :return: Lista de diccionarios con la información de los mantenimientos.
        """
        query = "SELECT * FROM Mantenimientos WHERE equipo_id=?"
        try:
            return self.db.fetch_query(query, (equipo_id,))
        except Exception as e:
            print(f"Error al obtener los mantenimientos por equipo: {e}")
            return []