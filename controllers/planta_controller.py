from models.planta_model import PlantasModel

class PlantaController:
    def __init__(self):
        # Crear una instancia del modelo prueba git
        self.plantas_model = PlantasModel()

    def obtener_plantas(self):
        """
        Obtiene los nombres de las plantas desde el modelo.
        
        :return: Lista de nombres de plantas.
        """
        plantas = self.plantas_model.get_all()
        return plantas if plantas else []  # Asegurar que no sea None