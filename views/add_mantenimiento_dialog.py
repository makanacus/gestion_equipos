from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox, QMessageBox, QDateEdit
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from controllers.mantenimiento_controller import MantenimientoController

class AddMantenimientoDialog(QDialog):
    def __init__(self, equipo_id):
        super().__init__()
        self.setWindowTitle("Agregar Mantenimiento")
        self.setFixedSize(400, 300)
        self.equipo_id = equipo_id
        self.controller = MantenimientoController()

        # Crear formulario
        layout = QFormLayout()

        self.fecha_mantenimiento_input = QDateEdit()
        self.fecha_mantenimiento_input.setDisplayFormat("yyyy-MM-dd")
        self.fecha_mantenimiento_input.setDate(QDate.currentDate())

        self.intervalo_mantenimiento_input = QLineEdit()
        self.intervalo_mantenimiento_input.setValidator(QIntValidator(1, 120))  # Solo enteros entre 1 y 120 meses

        self.recambios_utilizados_input = QLineEdit()
        self.descripcion_input = QTextEdit()

        # Añadir campos al formulario
        layout.addRow("Fecha Mantenimiento:", self.fecha_mantenimiento_input)
        layout.addRow("Intervalo Mantenimiento (meses):", self.intervalo_mantenimiento_input)
        layout.addRow("Recambios Utilizados:", self.recambios_utilizados_input)
        layout.addRow("Descripción:", self.descripcion_input)

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
        Valida si los campos obligatorios están completos.
        """
        if not self.fecha_mantenimiento_input.date().isValid():
            self.show_error_message("La fecha de mantenimiento es obligatoria y debe ser válida.")
            return False
        if not self.descripcion_input.toPlainText().strip():
            self.show_error_message("La descripción es obligatoria.")
            return False
        return True

    def show_error_message(self, message):
        """
        Muestra un mensaje de error si hay un campo vacío.
        """
        QMessageBox.critical(self, "Error", message)

    def accept(self):
        if self.validate_fields():
            fecha_mantenimiento = self.fecha_mantenimiento_input.date().toString("yyyy-MM-dd")

            # Convertir intervalo a entero si no está vacío
            intervalo_text = self.intervalo_mantenimiento_input.text().strip()
            intervalo_mantenimiento = int(intervalo_text) if intervalo_text else None
            
            recambios_utilizados = self.recambios_utilizados_input.text().strip() or None
            descripcion = self.descripcion_input.toPlainText().strip()

            exito = self.controller.crear_mantenimiento(
                self.equipo_id,
                fecha_mantenimiento,
                intervalo_mantenimiento,
                recambios_utilizados,
                descripcion
            )

            if exito:
                QMessageBox.information(self, "Éxito", "Mantenimiento agregado correctamente.")
                super().accept()
            else:
                self.show_error_message("Hubo un error al agregar el mantenimiento.")
