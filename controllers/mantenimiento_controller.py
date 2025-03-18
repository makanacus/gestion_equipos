from models.mantenimiento_model import MantenimientoModel


class MantenimientoController:
    def __init__(self):
        self.model = MantenimientoModel()

    def crear_mantenimiento(self, equipo_id, fecha_mantenimiento, intervalo_mantenimiento, recambios_utilizados, descripcion):
        """
        Crea un nuevo mantenimiento.
        
        :param equipo_id: ID del equipo.
        :param fecha_mantenimiento: Fecha del mantenimiento.
        :param intervalo_mantenimiento: Intervalo en meses para el próximo mantenimiento.
        :param recambios_utilizados: Recambios utilizados (puede ser NULL).
        :param descripcion: Descripción del mantenimiento.
        :return: True si se creó correctamente, False en caso de error.
        """
        try:
            self.model.create(equipo_id, fecha_mantenimiento, intervalo_mantenimiento, recambios_utilizados, descripcion)
            return True
        except Exception as e:
            print(f"Error en el controlador al crear mantenimiento: {e}")
            return False

    def actualizar_mantenimiento(self, mantenimiento_id, fecha_mantenimiento=None, intervalo_mantenimiento=None, recambios_utilizados=None, descripcion=None):
        """
        Actualiza un mantenimiento existente.
        
        :param mantenimiento_id: ID del mantenimiento a actualizar.
        :param fecha_mantenimiento: Nueva fecha de mantenimiento (opcional).
        :param intervalo_mantenimiento: Nuevo intervalo de mantenimiento (opcional).
        :param recambios_utilizados: Nuevos recambios utilizados (opcional).
        :param descripcion: Nueva descripción (opcional).
        :return: True si se actualizó correctamente, False en caso de error.
        """
        try:
            self.model.update(mantenimiento_id, fecha_mantenimiento, intervalo_mantenimiento, recambios_utilizados, descripcion)
            return True
        except Exception as e:
            print(f"Error en el controlador al actualizar mantenimiento: {e}")
            return False

    def eliminar_mantenimiento(self, mantenimiento_id):
        """
        Elimina un mantenimiento.
        
        :param mantenimiento_id: ID del mantenimiento a eliminar.
        :return: True si se eliminó correctamente, False en caso de error.
        """
        try:
            self.model.delete(mantenimiento_id)
            return True
        except Exception as e:
            print(f"Error en el controlador al eliminar mantenimiento: {e}")
            return False

    def obtener_mantenimiento_por_id(self, mantenimiento_id):
        """
        Obtiene un mantenimiento por su ID.
        
        :param mantenimiento_id: ID del mantenimiento.
        :return: Diccionario con la información del mantenimiento o None si no se encuentra.
        """
        try:
            return self.model.get_by_id(mantenimiento_id)
        except Exception as e:
            print(f"Error en el controlador al obtener mantenimiento por ID: {e}")
            return None

    def obtener_todos_los_mantenimientos(self):
        """
        Obtiene todos los mantenimientos.
        
        :return: Lista de diccionarios con la información de los mantenimientos.
        """
        try:
            return self.model.get_all()
        except Exception as e:
            print(f"Error en el controlador al obtener todos los mantenimientos: {e}")
            return []

    def obtener_mantenimientos_por_equipo(self, equipo_id):
        """
        Obtiene todos los mantenimientos asociados a un equipo.
        
        :param equipo_id: ID del equipo.
        :return: Lista de diccionarios con la información de los mantenimientos.
        """
        try:
            return self.model.get_by_equipo(equipo_id)
        except Exception as e:
            print(f"Error en el controlador al obtener mantenimientos por equipo: {e}")
            return []