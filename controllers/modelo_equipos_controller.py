from models.modelo_equipos_model import ModeloEquiposModel

class ModeloEquiposController:
    def __init__(self):
        self.model = ModeloEquiposModel()

    def create_modelo(self, nombre):
        """
        Crea un nuevo modelo de equipo en la base de datos.
        
        :param nombre: Nombre del modelo.
        :return: None
        """
        return self.model.create(nombre)

    def get_all_modelos(self):
        """
        Obtiene todos los modelos de equipos y los retorna como una lista de diccionarios.
        
        :return: Lista de diccionarios con la información de los modelos.
        """
        resultados = self.model.get_all()  # Suponiendo que devuelve una lista de tuplas

        # Convertir lista de tuplas en lista de diccionarios
        modelos = [{"id_modelo": row[0], "nombre": row[1]} for row in resultados]

        return modelos

    def get_modelo_by_id(self, id_modelo):
        """
        Obtiene un modelo de equipo por su ID.
        
        :param id_modelo: ID del modelo.
        :return: Diccionario con la información del modelo o None si no se encuentra.
        """
        return self.model.get_by_id(id_modelo)

    def get_modelo_by_nombre(self, nombre):
        """
        Obtiene un modelo de equipo por su nombre.
        
        :param nombre: Nombre del modelo.
        :return: Diccionario con la información del modelo o None si no se encuentra.
        """
        return self.model.get_by_nombre(nombre)