from database import Database

class PlantasModel:
    def __init__(self):
        self.db = Database()

    def create(self, nombre):
        """
        Crea una nueva planta en la base de datos.
        
        :param nombre: Nombre de la planta.
        :return: None
        """
        query = """INSERT INTO Plantas (nombre)
                   VALUES (?)"""
        try:
            self.db.execute_query(query, (nombre,))
            print(f"Planta '{nombre}' creada correctamente.")
        except Exception as e:
            print(f"Error al crear la planta: {e}")

    def get_all(self):
        """
        Obtiene todas las plantas de la base de datos.
        
        :return: Lista de tuplas con la información de las plantas.
        """
        query = "SELECT id_planta, nombre FROM Plantas"
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener las plantas: {e}")
            return []

    def get_by_id(self, id_planta):
        """
        Obtiene una planta por su ID.
        
        :param id_planta: ID de la planta.
        :return: Diccionario con la información de la planta o None si no se encuentra.
        """
        query = "SELECT * FROM Plantas WHERE id_planta=?"
        try:
            result = self.db.fetch_query(query, (id_planta,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró la planta con ID '{id_planta}'.")
                return None
        except Exception as e:
            print(f"Error al obtener la planta por ID: {e}")
            return None

    def get_by_nombre(self, nombre):
        """
        Obtiene una planta por su nombre.
        
        :param nombre: Nombre de la planta.
        :return: Diccionario con la información de la planta o None si no se encuentra.
        """
        query = "SELECT * FROM Plantas WHERE nombre=?"
        try:
            result = self.db.fetch_query(query, (nombre,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró la planta con nombre '{nombre}'.")
                return None
        except Exception as e:
            print(f"Error al obtener la planta por nombre: {e}")
            return None