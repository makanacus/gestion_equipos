from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QMessageBox
from controllers.planta_controller import PlantaController

class UpdateEquipoDialog(QDialog):
    def __init__(self, equipo_id, equipo_data, controller):
        super().__init__()
        self.setWindowTitle("Modificar Equipo")
        self.setFixedSize(400, 300)

        self.equipo_id = equipo_id
        self.controller = controller
        self.equipo_data = equipo_data  # Guardar los datos para usarlos después

        # Crear formulario
        layout = QFormLayout()

        # Campos de solo lectura
        self.id_input = QLineEdit(equipo_data['id'])
        self.id_input.setReadOnly(True)

        self.equipo_input = QLineEdit(equipo_data['equipo'])
        self.equipo_input.setReadOnly(True)

        self.modelo_input = QLineEdit(equipo_data['modelo'])
        self.modelo_input.setReadOnly(True)

        # Campos modificables
        self.ubicacion_input = QComboBox()
        self.estado_input = QComboBox()
        self.estado_input.addItems(["Activo", "Inactivo"])

        # Cargar las plantas dinámicamente (esto establecerá la selección automáticamente)
        self.cargar_plantas()

        # Añadir campos al formulario
        layout.addRow("Id:", self.id_input)
        layout.addRow("Equipo:", self.equipo_input)
        layout.addRow("Modelo:", self.modelo_input)
        layout.addRow("Ubicación:", self.ubicacion_input)
        layout.addRow("Estado:", self.estado_input)

        # Crear botones
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Añadir botones al formulario
        layout.addWidget(self.button_box)

        # Establecer el layout
        self.setLayout(layout)

    def accept(self):
        """
        Guarda los cambios en la ubicación y el estado.
        """
        self.controller.update_equipo(
            self.equipo_id,
            id_planta=self.ubicacion_input.currentData(),
            estado=self.estado_input.currentText()
        )
        QMessageBox.information(self, "Éxito", "Equipo actualizado correctamente.")
        super().accept()

    def cargar_plantas(self):
        """
        Carga las plantas desde el controlador y establece la selección actual.
        """
        plantas_controller = PlantaController()
        plantas = plantas_controller.obtener_plantas()

        self.ubicacion_input.clear()

        current_index = -1
        for idx, planta in enumerate(plantas):
            # Asumimos que 'planta' es una tupla (id_planta, nombre)
            self.ubicacion_input.addItem(planta[1], planta[0])
            
            # Verificar si esta es la planta actual del equipo
            if str(planta[0]) == str(self.equipo_data.get('id_planta')):
                current_index = idx
            elif planta[1] == self.equipo_data.get('ubicacion'):
                current_index = idx

        # Establecer la selección después de cargar todos los items
        if current_index >= 0:
            self.ubicacion_input.setCurrentIndex(current_index)

        # Establecer el estado
        estado_text = self.equipo_data.get('estado', 'Activo')
        estado_index = self.estado_input.findText(estado_text)
        if estado_index >= 0:
            self.estado_input.setCurrentIndex(estado_index)