from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class UpdateRecambioDialog(QDialog):
    def __init__(self, recambio_id, recambio_data, controller):
        super().__init__()
        self.recambio_id = recambio_id
        self.controller = controller
        self.recambio_data = recambio_data
        self.setWindowTitle("Actualizar Recambio")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.modelo_equipo_input = QLineEdit(self.recambio_data['modelo_equipo'])
        layout.addWidget(QLabel("Modelo Equipo:"))
        layout.addWidget(self.modelo_equipo_input)

        self.recambio_input = QLineEdit(self.recambio_data['recambio'])
        layout.addWidget(QLabel("Recambio:"))
        layout.addWidget(self.recambio_input)

        self.cantidad_input = QLineEdit(str(self.recambio_data['cantidad']))
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)

        self.cantidad_minima_input = QLineEdit(str(self.recambio_data['cantidad_minima']))
        layout.addWidget(QLabel("Cantidad Mínima:"))
        layout.addWidget(self.cantidad_minima_input)

        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)