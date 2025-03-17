from models.recambios_modelos_model import RecambiosModelosModel

class RecambiosModelosController:
    def __init__(self):
        self.model = RecambiosModelosModel()

    def create_relacion(self, id_recambio, id_modelo):
        """
        Crea una nueva relación entre un recambio y un modelo.
        
        :param id_recambio: ID del recambio.
        :param id_modelo: ID del modelo.
        :return: None
        """
        return self.model.create(id_recambio, id_modelo)

    def get_all_relaciones(self):
        """
        Obtiene todas las relaciones entre recambios y modelos.
        
        :return: Lista de diccionarios con la información de las relaciones.
        """
        return self.model.get_all()

    def get_relaciones_by_recambio(self, id_recambio):
        """
        Obtiene todas las relaciones asociadas a un recambio específico.
        
        :param id_recambio: ID del recambio.
        :return: Lista de diccionarios con la información de las relaciones.
        """
        return self.model.get_by_recambio(id_recambio)

    def get_relaciones_by_modelo(self, id_modelo):
        """
        Obtiene todas las relaciones asociadas a un modelo específico.
        
        :param id_modelo: ID del modelo.
        :return: Lista de diccionarios con la información de las relaciones.
        """
        return self.model.get_by_modelo(id_modelo)

    def update_relacion(self, id_recambio, nuevos_modelos):
        """
        Actualiza las relaciones de un recambio con los modelos.
        
        :param id_recambio: ID del recambio a actualizar.
        :param nuevos_modelos: Lista de nuevos IDs de modelos.
        :return: True si se actualizó correctamente, False en caso de error.
        """
        return self.model.update_relaciones_by_recambio(id_recambio, nuevos_modelos)


    def delete_relacion(self, id_recambio, id_modelo):
        """
        Elimina una relación entre un recambio y un modelo.
        
        :param id_recambio: ID del recambio.
        :param id_modelo: ID del modelo.
        :return: None
        """
        return self.model.delete(id_recambio, id_modelo)