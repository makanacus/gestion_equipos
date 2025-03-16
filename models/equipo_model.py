from database import Database

class EquipoModel:
    def __init__(self):
        self.db = Database()

    def create(self, id, equipo, modelo, ubicacion, estado):
        """
        Crea un nuevo equipo en la base de datos.
        
        :param id: Identificador único del equipo.
        :param equipo: Nombre del equipo.
        :param modelo: Modelo del equipo.
        :param ubicacion: Ubicación del equipo.
        :param estado: Estado del equipo (Activo/Inactivo).
        :return: None
        """
        query = """INSERT INTO Equipos (id, equipo, modelo, ubicacion, estado)
                   VALUES (?, ?, ?, ?, ?)"""
        try:
            self.db.execute_query(query, (id, equipo, modelo, ubicacion, estado))
            print(f"Equipo '{equipo}' creado correctamente.")
        except Exception as e:
            print(f"Error al crear el equipo: {e}")

    def update(self, equipo_id, equipo=None, modelo=None, ubicacion=None, estado=None):
        """
        Actualiza la información de un equipo existente.
        
        :param equipo_id: Identificador único del equipo a actualizar.
        :param equipo: Nuevo nombre del equipo (opcional).
        :param modelo: Nuevo modelo del equipo (opcional).
        :param ubicacion: Nueva ubicación del equipo (opcional).
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
        if ubicacion:
            updates.append("ubicacion=?")
            params.append(ubicacion)
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
        Obtiene un equipo por su ID.
        
        :param equipo_id: Identificador único del equipo.
        :return: Diccionario con la información del equipo o None si no se encuentra.
        """
        query = "SELECT * FROM Equipos WHERE id=?"
        try:
            result = self.db.fetch_query(query, (equipo_id,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró el equipo con ID '{equipo_id}'.")
                return None
        except Exception as e:
            print(f"Error al obtener el equipo: {e}")
            return None

    def get_all(self):
        """
        Obtiene todos los equipos de la base de datos.
        
        :return: Lista de diccionarios con la información de los equipos.
        """
        query = "SELECT * FROM Equipos"
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener los equipos: {e}")
            return []

    def get_by_ubicacion(self, ubicacion):
        """
        Obtiene todos los equipos en una ubicación específica.
        
        :param ubicacion: Ubicación de los equipos a buscar.
        :return: Lista de diccionarios con la información de los equipos.
        """
        query = "SELECT * FROM Equipos WHERE ubicacion=?"
        try:
            return self.db.fetch_query(query, (ubicacion,))
        except Exception as e:
            print(f"Error al obtener los equipos por ubicación: {e}")
            return []