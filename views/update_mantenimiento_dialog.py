from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox, QMessageBox, QDateEdit
)
from PyQt6.QtCore import QDate
from controllers.mantenimiento_controller import MantenimientoController

class UpdateMantenimientoDialog(QDialog):
    def __init__(self, mantenimiento):
        """
        mantenimiento: una tupla con los datos del mantenimiento (id, equipo_id, fecha_mantenimiento, intervalo, proximo_mantenimiento, recambios_utilizados, descripcion)
        """
        super().__init__()
        self.setWindowTitle("Modificar Mantenimiento")
        self.setFixedSize(400, 300)

        self.mantenimiento_id = mantenimiento[0]
        self.controller = MantenimientoController()

        # Crear formulario
        layout = QFormLayout()

        self.fecha_mantenimiento_input = QDateEdit()
        self.fecha_mantenimiento_input.setDisplayFormat("yyyy-MM-dd")
        self.fecha_mantenimiento_input.setDate(QDate.fromString(mantenimiento[2], "yyyy-MM-dd"))

        self.intervalo_mantenimiento_input = QLineEdit(str(mantenimiento[3]) if mantenimiento[3] else "")
        self.recambios_utilizados_input = QLineEdit(mantenimiento[5] if mantenimiento[5] else "")
        self.descripcion_input = QTextEdit(mantenimiento[6] if mantenimiento[6] else "")

        # Añadir campos al formulario
        layout.addRow("Fecha Mantenimiento:", self.fecha_mantenimiento_input)
        layout.addRow("Intervalo Mantenimiento (meses):", self.intervalo_mantenimiento_input)
        layout.addRow("Recambios Utilizados:", self.recambios_utilizados_input)
        layout.addRow("Descripción:", self.descripcion_input)

        # Crear botones
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def validate_fields(self):
        """
        Valida si los campos obligatorios están completos y correctos.
        """
        if not self.fecha_mantenimiento_input.date().isValid():
            self.show_error_message("La fecha de mantenimiento es obligatoria y debe ser válida.")
            return False
        if not self.intervalo_mantenimiento_input.text().strip().isdigit():
            self.show_error_message("El intervalo de mantenimiento debe ser un número entero.")
            return False
        if not self.descripcion_input.toPlainText().strip():
            self.show_error_message("La descripción es obligatoria.")
            return False
        return True

    def show_error_message(self, message):
        """
        Muestra un mensaje de error si hay un campo incorrecto.
        """
        QMessageBox.critical(self, "Error", message)

    def accept(self):
        if self.validate_fields():
            fecha_mantenimiento = self.fecha_mantenimiento_input.date().toString("yyyy-MM-dd")
            intervalo_mantenimiento = int(self.intervalo_mantenimiento_input.text().strip())
            recambios_utilizados = self.recambios_utilizados_input.text().strip() or None
            descripcion = self.descripcion_input.toPlainText().strip()

            exito = self.controller.actualizar_mantenimiento(
                self.mantenimiento_id,
                fecha_mantenimiento,
                intervalo_mantenimiento,
                recambios_utilizados,
                descripcion
            )

            if exito:
                QMessageBox.information(self, "Éxito", "Mantenimiento modificado correctamente.")
                super().accept()
            else:
                self.show_error_message("Hubo un error al modificar el mantenimiento.")
