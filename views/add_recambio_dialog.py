from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QIntValidator
from controllers.modelo_equipos_controller import ModeloEquiposController
from controllers.recambio_controller import RecambioController
from controllers.recambios_modelos_controller import RecambiosModelosController

class AddRecambioDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Recambio")
        self.setFixedSize(400, 300)

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

    def cargar_modelos(self):
        """
        Carga los modelos desde la base de datos y los añade a la lista,
        guardando el id_modelo en el item para uso posterior.
        """
        modelos = self.modelo_controller.get_all_modelos()
        for modelo in modelos:
            item = QListWidgetItem(modelo["nombre"])  # Mostrar el nombre al usuario
            item.setData(1, modelo["id_modelo"])  # Guardar el ID como dato oculto
            self.modelos_list.addItem(item)

    def validate_fields(self):
        """
        Valida si todos los campos están completos y son válidos.
        """
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
        """
        Muestra un mensaje de error.
        """
        QMessageBox.critical(self, "Error", message)

    def accept(self):
        """
        Intenta guardar el recambio y sus relaciones con modelos.
        Si algo falla, no guarda nada y muestra un mensaje de error.
        """
        if self.validate_fields():
            # Obtener datos del formulario
            recambio = self.recambio_input.text().strip()
            cantidad = int(self.cantidad_input.text())
            cantidad_minima = int(self.cantidad_minima_input.text())

            # Obtener los IDs de los modelos seleccionados
            modelos_seleccionados = [item.data(1) for item in self.modelos_list.selectedItems()]

            # Iniciar proceso de guardado
            try:
                # Crear el recambio y obtener su ID
                recambio_id = self.recambio_controller.create_recambio(
                    recambio=recambio,
                    cantidad=cantidad,
                    cantidad_minima=cantidad_minima
                )

                if not recambio_id:
                    raise Exception("No se pudo crear el recambio en la base de datos.")

                # Crear relaciones entre el recambio y los modelos seleccionados
                for id_modelo in modelos_seleccionados:
                    prueba = self.recambios_modelos_controller.create_relacion(recambio_id, id_modelo)
                    if not prueba:
                        raise Exception(f"No se pudo registrar la relación con el modelo ID {id_modelo}")

                # Si todo salió bien, mostrar mensaje de éxito y cerrar
                QMessageBox.information(self, "Éxito", "Recambio agregado correctamente.")
                super().accept()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
