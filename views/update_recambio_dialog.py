from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QIntValidator
from controllers.modelo_equipos_controller import ModeloEquiposController
from controllers.recambio_controller import RecambioController
from controllers.recambios_modelos_controller import RecambiosModelosController

class UpdateRecambioDialog(QDialog):
    def __init__(self, recambio_id):
        super().__init__()
        self.setWindowTitle("Actualizar Recambio")
        self.setFixedSize(400, 300)
        self.recambio_id = recambio_id

        # Controladores
        self.modelo_controller = ModeloEquiposController()
        self.recambio_controller = RecambioController()
        self.recambios_modelos_controller = RecambiosModelosController()

        # Crear formulario
        layout = QFormLayout()

        # Campo de texto para el nombre del recambio
        self.recambio_input = QLineEdit()
        layout.addRow("Recambio:", self.recambio_input)

        # Lista de modelos con selección múltiple
        self.modelos_list = QListWidget()
        self.modelos_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.cargar_modelos()
        layout.addRow("Modelos que incluyen recambio:", self.modelos_list)

        # Campo de texto para la cantidad
        self.cantidad_input = QLineEdit()
        self.cantidad_input.setValidator(QIntValidator())
        layout.addRow("Cantidad:", self.cantidad_input)

        # Campo de texto para la cantidad mínima
        self.cantidad_minima_input = QLineEdit()
        self.cantidad_minima_input.setValidator(QIntValidator())
        layout.addRow("Cantidad mínima:", self.cantidad_minima_input)

        # Botones de aceptar y cancelar
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        self.cargar_datos()

    def cargar_modelos(self):
        modelos = self.modelo_controller.get_all_modelos()
        for modelo in modelos:
            item = QListWidgetItem(modelo["nombre"]) # Mostrar el nombre al usuario
            item.setData(1, modelo["id_modelo"]) # Guardar el ID como dato oculto
            self.modelos_list.addItem(item)

    def cargar_datos(self):
        recambio = self.recambio_controller.get_recambio_by_id(self.recambio_id)
        if recambio:
            self.recambio_input.setText(recambio["recambio"])
            self.cantidad_input.setText(str(recambio["cantidad"]))
            self.cantidad_minima_input.setText(str(recambio["cantidad_minima"]))
            modelos_asociados = self.recambios_modelos_controller.get_relaciones_by_recambio(self.recambio_id)
            modelos_asociados = [modelo[1] for modelo in modelos_asociados]
            for i in range(self.modelos_list.count()):
                item = self.modelos_list.item(i)
                modelo_id = item.data(1)  # Obtiene el ID almacenado en el item

                print(f"Comparando: modelo_id {modelo_id} con modelos_asociados {modelos_asociados}")

                if modelo_id in modelos_asociados:
                    print(f"¡Match encontrado! Seleccionando modelo_id: {modelo_id}")
                    item.setSelected(True)

    def validate_fields(self):
        if not self.recambio_input.text().strip():
            self.show_error_message("El nombre del recambio es obligatorio.")
            return False
        if not self.modelos_list.selectedItems():
            self.show_error_message("Debe seleccionar al menos un modelo.")
            return False
        if not self.cantidad_input.text().strip():
            self.show_error_message("La cantidad es obligatoria.")
            return False
        if not self.cantidad_minima_input.text().strip():
            self.show_error_message("La cantidad mínima es obligatoria.")
            return False
        return True

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def accept(self):
        if self.validate_fields():
            recambio = self.recambio_input.text().strip()
            cantidad = int(self.cantidad_input.text())
            cantidad_minima = int(self.cantidad_minima_input.text())
            modelos_seleccionados = [item.data(1) for item in self.modelos_list.selectedItems()]
            
            try:
                # Actualizar datos del recambio
                actualizado = self.recambio_controller.update_recambio(
                    recambio_id=self.recambio_id,
                    recambio=recambio,
                    cantidad=cantidad,
                    cantidad_minima=cantidad_minima
                )

                if not actualizado:
                    raise Exception("No se pudo actualizar el recambio.")

                # Actualizar las relaciones del recambio con los modelos
                relaciones_actualizadas = self.recambios_modelos_controller.update_relacion(self.recambio_id, modelos_seleccionados)

                if not relaciones_actualizadas:
                    raise Exception("No se pudieron actualizar las relaciones del recambio con los modelos.")

                # Confirmación de éxito
                QMessageBox.information(self, "Éxito", "Recambio y relaciones actualizados correctamente.")
                super().accept()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
