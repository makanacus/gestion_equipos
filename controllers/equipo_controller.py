from models.equipo_model import EquipoModel

class EquipoController:
    def __init__(self):
        self.model = EquipoModel()

    def create_equipo(self, id, equipo, modelo, ubicacion, estado):
        return self.model.create(id, equipo, modelo, ubicacion, estado)

    def update_equipo(self, equipo_id, equipo=None, modelo=None, ubicacion=None, estado=None):
        return self.model.update(equipo_id, equipo, modelo, ubicacion, estado)

    def delete_equipo(self, equipo_id):
        return self.model.delete(equipo_id)

    def get_equipo_by_id(self, equipo_id):
        return self.model.get_by_id(equipo_id)

    def get_all_equipos(self):
        return self.model.get_all()

    def get_equipos_by_ubicacion(self, ubicacion):
        return self.model.get_by_ubicacion(ubicacion)