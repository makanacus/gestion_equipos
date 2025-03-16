from database import Database

class ModeloEquiposModel:
    def __init__(self):
        self.db = Database()

    def create(self, nombre):
        """
        Crea un nuevo modelo de equipo en la base de datos.
        
        :param nombre: Nombre del modelo.
        :return: None
        """
        query = """INSERT INTO Modelo_equipos (nombre)
                   VALUES (?)"""
        try:
            self.db.execute_query(query, (nombre,))
            print(f"Modelo '{nombre}' creado correctamente.")
        except Exception as e:
            print(f"Error al crear el modelo: {e}")

    def get_all(self):
        """
        Obtiene todos los modelos de equipos.
        
        :return: Lista de diccionarios con la información de los modelos.
        """
        query = "SELECT * FROM Modelo_equipos"
        try:
            return self.db.fetch_query(query)
        except Exception as e:
            print(f"Error al obtener los modelos: {e}")
            return []

    def get_by_id(self, id_modelo):
        """
        Obtiene un modelo de equipo por su ID.
        
        :param id_modelo: ID del modelo.
        :return: Diccionario con la información del modelo o None si no se encuentra.
        """
        query = "SELECT * FROM Modelo_equipos WHERE id_modelo=?"
        try:
            result = self.db.fetch_query(query, (id_modelo,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró el modelo con ID '{id_modelo}'.")
                return None
        except Exception as e:
            print(f"Error al obtener el modelo por ID: {e}")
            return None

    def get_by_nombre(self, nombre):
        """
        Obtiene un modelo de equipo por su nombre.
        
        :param nombre: Nombre del modelo.
        :return: Diccionario con la información del modelo o None si no se encuentra.
        """
        query = "SELECT * FROM Modelo_equipos WHERE nombre=?"
        try:
            result = self.db.fetch_query(query, (nombre,))
            if result:
                return result[0]  # Devuelve el primer registro encontrado
            else:
                print(f"No se encontró el modelo con nombre '{nombre}'.")
                return None
        except Exception as e:
            print(f"Error al obtener el modelo por nombre: {e}")
            return None