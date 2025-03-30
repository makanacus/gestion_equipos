from database import Database

class EquipoModel:
    def __init__(self):
        self.db = Database()

    def create(self, id, equipo, modelo, id_planta, estado):
        """
        Crea un nuevo equipo en la base de datos.
        
        :param id: Identificador único del equipo.
        :param equipo: Nombre del equipo.
        :param modelo: Modelo del equipo.
        :param id_planta: id_planta del equipo.
        :param estado: Estado del equipo (Activo/Inactivo).
        :return: None
        """
        query = """INSERT INTO Equipos (id, equipo, modelo, id_planta, estado)
                   VALUES (?, ?, ?, ?, ?)"""
        try:
            self.db.execute_query(query, (id, equipo, modelo, id_planta, estado))
            print(f"Equipo '{equipo}' creado correctamente.")
        except Exception as e:
            print(f"Error al crear el equipo: {e}")

    def update(self, equipo_id, equipo=None, modelo=None, id_planta=None, estado=None):
        """
        Actualiza la información de un equipo existente.
        
        :param equipo_id: Identificador único del equipo a actualizar.
        :param equipo: Nuevo nombre del equipo (opcional).
        :param modelo: Nuevo modelo del equipo (opcional).
        :param id_planta: Nuevo id_planta del equipo (opcional).
        :param estado: Nuevo estado del equipo (opcional).
        :return: None
        """
        updates = []
        params = []

        if equipo:
            updates.append("equipo=?")
            params.append(equipo)
        if modelo:
            updates.append("modelo=?")
            params.append(modelo)
        if id_planta:
            updates.append("id_planta=?")
            params.append(id_planta)
        if estado:
            updates.append("estado=?")
            params.append(estado)

        if not updates:
            print("No se proporcionaron datos para actualizar.")
            return

        query = f"UPDATE Equipos SET {', '.join(updates)} WHERE id=?"
        params.append(equipo_id)

        try:
            self.db.execute_query(query, tuple(params))
            print(f"Equipo con ID '{equipo_id}' actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar el equipo: {e}")

    def delete(self, equipo_id):
        """
        Elimina un equipo de la base de datos.
        
        :param equipo_id: Identificador único del equipo a eliminar.
        :return: None
        """
        query = "DELETE FROM Equipos WHERE id=?"
        try:
            self.db.execute_query(query, (equipo_id,))
            print(f"Equipo con ID '{equipo_id}' eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar el equipo: {e}")

    def get_by_id(self, equipo_id):
        """
        Obtiene un equipo por su ID con el nombre de la planta.
        
        :param equipo_id: Identificador único del equipo.
        :return: Diccionario con la información del equipo o None si no se encuentra.
        """
        query = """SELECT e.id, e.equipo, e.modelo, p.nombre as planta, e.estado
                   FROM Equipos e
                   JOIN Plantas p ON e.id_planta = p.id_planta
                   WHERE e.id = ?"""
        try:
            result = self.db.fetch_query(query, (equipo_id,))
            return result[0] if result else None
        except Exception as e:
            print(f"Error al obtener el equipo con planta: {e}")
            return None

    def get_all(self):
        """
        Obtiene todos los equipos de la base de datos con el nombre de la planta incluida.
        
        :return: Lista de diccionarios con la información de los equipos.
        """
        query = """SELECT e.id, e.equipo, e.modelo, p.nombre as planta, e.estado
                   FROM Equipos e
                   JOIN Plantas p ON e.id_planta = p.id_planta"""
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener los equipos con plantas: {e}")
            return []

    def get_by_id_planta(self, id_planta):
        """
        Obtiene todos los equipos en una ubicación específica, incluyendo el nombre de la planta.
        
        :param id_planta: ID de la planta.
        :return: Lista de diccionarios con la información de los equipos.
        """
        query = """SELECT e.id, e.equipo, e.modelo, p.nombre as planta, e.estado
                FROM Equipos e
                JOIN Plantas p ON e.id_planta = p.id_planta
                WHERE e.id_planta = ?"""
        try:
            return self.db.fetch_query(query, (id_planta,))
        except Exception as e:
            print(f"Error al obtener los equipos por id_planta: {e}")
            return []
