from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QListWidgetItem, QWidget, QHBoxLayout, QLabel
)
from controllers.recambios_modelos_controller import RecambiosModelosController
from controllers.recambio_controller import RecambioController


class RepuestosEquipoDialog(QDialog):
    def __init__(self, equipo_id, modelo_id):
        super().__init__()
        self.setWindowTitle(f"Repuestos para Equipo {equipo_id}")
        self.setFixedSize(400, 300)

        self.modelo_id = modelo_id
        self.recambios_controller = RecambioController()
        self.recambios_modelos_controller = RecambiosModelosController()

        layout = QVBoxLayout()

        # Lista de repuestos
        self.repuestos_list = QListWidget()
        layout.addWidget(self.repuestos_list)

        # Botón para cerrar
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        # Cargar repuestos
        self.cargar_repuestos()

        self.setLayout(layout)

    def cargar_repuestos(self):
        """
        Carga y muestra los repuestos asociados al modelo del equipo.
        Muestra un punto verde si el stock es correcto y rojo si es bajo.
        """
        self.repuestos_list.clear()
        relaciones = self.recambios_modelos_controller.get_relaciones_by_modelo(self.modelo_id)

        if not relaciones:
            QMessageBox.information(self, "Sin repuestos", "No hay repuestos asociados a este modelo.")
            return

        for relacion in relaciones:
            # Si relacion es una tupla, accede por índice en lugar de clave
            if isinstance(relacion, tuple):
                id_recambio = relacion[0]  # Asegúrate de que el índice es correcto
            else:
                id_recambio = relacion['id_recambio']  # Si es un diccionario

            recambio = self.recambios_controller.get_recambio_by_id(id_recambio)
            if recambio:
                # Crear un widget personalizado para el item
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                item_widget.setLayout(item_layout)

                # Crear un punto de color
                punto = QLabel()
                punto.setFixedSize(10, 10)  # Tamaño del punto
                if recambio.get('stock_bajo', False):  # Stock bajo
                    punto.setStyleSheet("background-color: red; border-radius: 5px;")
                else:  # Stock correcto
                    punto.setStyleSheet("background-color: green; border-radius: 5px;")
                item_layout.addWidget(punto)

                # Texto del recambio
                texto = QLabel(f"{recambio['recambio']} (Cantidad: {recambio['cantidad']})")
                item_layout.addWidget(texto)
                item_layout.addStretch()  # Alinear a la izquierda

                # Crear un QListWidgetItem y asignarle el widget personalizado
                item = QListWidgetItem()
                item.setSizeHint(item_widget.sizeHint())  # Ajustar el tamaño del item
                self.repuestos_list.addItem(item)
                self.repuestos_list.setItemWidget(item, item_widget)