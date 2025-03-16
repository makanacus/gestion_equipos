from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
from controllers.planta_controller import PlantaController

class UpdateEquipoDialog(QDialog):
    def __init__(self, equipo_id, equipo_data, equipo_model):
        super().__init__()
        self.setWindowTitle("Modificar Equipo")
        self.setFixedSize(400, 300)

        self.equipo_id = equipo_id
        self.equipo_model = equipo_model

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

        # Cargar valores actuales
        self.ubicacion_input.setCurrentText(equipo_data['ubicacion'])
        self.estado_input.setCurrentText(equipo_data['estado'])

        # Cargar las plantas dinámicamente
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
        self.equipo_model.update(
            self.equipo_id,
            ubicacion=self.ubicacion_input.currentText(),
            estado=self.estado_input.currentText()
        )
        super().accept()

    def cargar_plantas(self):
        """
        Carga las plantas desde el controlador y las añade al QComboBox.
        """
        plantas_controller = PlantaController()
        nombres_plantas = plantas_controller.obtener_plantas()
        self.ubicacion_input.clear()
        self.ubicacion_input.addItems(nombres_plantas)
