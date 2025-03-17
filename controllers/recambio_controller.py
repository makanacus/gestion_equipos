from models.recambio_model import RecambioModel

class RecambioController:
    def __init__(self):
        self.model = RecambioModel()

    def create_recambio(self, recambio, cantidad, cantidad_minima):
        """
        Crea un nuevo recambio y lo guarda en la base de datos.

        :param recambio: Nombre del recambio.
        :param cantidad: Cantidad disponible.
        :param cantidad_minima: Cantidad mínima de stock.
        :return: ID del recambio creado o None si hubo un error.
        """
        return self.model.create(recambio, cantidad, cantidad_minima)

    def update_recambio(self, recambio_id, recambio=None, cantidad=None, cantidad_minima=None):
        """
        Actualiza un recambio existente.

        :param recambio_id: ID del recambio a actualizar.
        :param recambio: Nuevo nombre del recambio (opcional).
        :param cantidad: Nueva cantidad disponible (opcional).
        :param cantidad_minima: Nueva cantidad mínima (opcional).
        :return: True si se actualizó correctamente, False en caso de error.
        """
        return self.model.update(recambio_id, recambio, cantidad, cantidad_minima)

    def delete_recambio(self, recambio_id):
        """
        Elimina un recambio de la base de datos.

        :param recambio_id: ID del recambio a eliminar.
        :return: True si se eliminó correctamente, False en caso de error.
        """
        return self.model.delete(recambio_id)

    def get_recambio_by_id(self, recambio_id):
        """
        Obtiene un recambio por su ID.

        :param recambio_id: ID del recambio.
        :return: Diccionario con los datos del recambio o None si no existe.
        """
        return self.model.get_by_id(recambio_id)

    def get_all_recambios(self):
        """
        Obtiene todos los recambios almacenados en la base de datos.

        :return: Lista de diccionarios con los datos de los recambios.
        """
        return self.model.get_all()

    def get_recambios_by_name(self, recambio):
        """
        Busca recambios por nombre.

        :param recambio: Parte del nombre del recambio a buscar.
        :return: Lista de diccionarios con los recambios encontrados.
        """
        return self.model.get_by_recambio(recambio)
