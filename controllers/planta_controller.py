from models.planta_model import PlantasModel

class PlantaController:
    def __init__(self):
        # Crear una instancia del modelo
        self.plantas_model = PlantasModel()

    def obtener_plantas(self):
        """
        Obtiene los nombres de las plantas desde el modelo.
        
        :return: Lista de nombres de plantas.
        """
        plantas = self.plantas_model.get_all()
        nombres_plantas = [planta[1] for planta in plantas]  # Acceder al segundo elemento de la tupla (nombre)
        return nombres_plantas