from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QMessageBox
from controllers.planta_controller import PlantaController

class AddEquipoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Equipo")
        
        self.setFixedSize(400, 300)

        # Crear formulario
        layout = QFormLayout()

        self.id_input = QLineEdit()
        self.equipo_input = QLineEdit()
        self.modelo_input = QLineEdit()
        self.ubicacion_input = QComboBox()
        self.estado_input = QComboBox()
        self.estado_input.addItems(["Activo", "Inactivo"])  # Ejemplo de estados

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

    def validate_fields(self):
        """
        Valida si todos los campos obligatorios están completos.
        Si falta algún campo, muestra un mensaje de error.
        """
        if not self.id_input.text().strip():
            self.show_error_message("El id es obligatorio.")
            return False
        if not self.equipo_input.text().strip():
            self.show_error_message("El equipo es obligatorio.")
            return False
        if not self.modelo_input.text().strip():
            self.show_error_message("El modelo es obligatorio.")
            return False
        if not self.ubicacion_input.currentText():
            self.show_error_message("La ubicación es obligatoria.")
            return False
        if not self.estado_input.currentText():
            self.show_error_message("El estado es obligatorio.")
            return False
        return True

    def show_error_message(self, message):
        """
        Muestra un mensaje de error si hay un campo vacío.
        """
        QMessageBox.critical(self, "Error", message)

    def accept(self):
        # Validamos antes de aceptar
        if self.validate_fields():

            # Pasar los datos validados a la ventana principal
            self.equipo_data = {
                'equipo': self.equipo_input.text().strip(),
                'modelo': self.modelo_input.text().strip(),
                'id_planta': self.ubicacion_input.currentData(),
                'estado': self.estado_input.currentText(),
            }
            # Si todo salió bien, mostrar mensaje de éxito y cerrar
            QMessageBox.information(self, "Éxito", "Equipo agregado correctamente.")
            super().accept()

    def get_equipo_data(self):
        """
        Devuelve los datos del equipo una vez que se haya aceptado el diálogo.
        """
        return self.equipo_data
    
    def cargar_plantas(self):
        """
        Carga las plantas desde el controlador y las añade al QComboBox.
        """
        # Crear una instancia del controlador
        plantas_controller = PlantaController()

        # Obtener los nombres de las plantas
        plantas = plantas_controller.obtener_plantas()
        # nombres_plantas = plantas_controller.obtener_plantas()

        # Limpiar el QComboBox antes de agregar nuevos elementos
        self.ubicacion_input.clear()

        # Agregar las plantas al QComboBox con sus IDs
        for planta in plantas:
            self.ubicacion_input.addItem(planta[1], planta[0])  # Añadir el nombre y almacenar el id

