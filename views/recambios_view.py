from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QAbstractItemView, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from views.add_recambio_dialog import AddRecambioDialog
from views.update_recambio_dialog import UpdateRecambioDialog
from controllers.recambio_controller import RecambioController
from functools import partial

class RecambiosView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.controller = RecambioController()  # Usar el controlador
        
        layout = QVBoxLayout()
        
        # Filtro de texto para buscar recambios
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Buscar recambio...")
        self.filter_input.textChanged.connect(self.load_recambios)  # Filtrar dinámicamente
        layout.addWidget(self.filter_input)
        
        # Tabla de recambios
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Recambio", "Cantidad", "Cantidad Mínima", "Stock" , "Acciones"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.table)
        
        # Botón para agregar recambio
        self.add_button = QPushButton("Agregar Recambio")
        self.add_button.clicked.connect(self.show_add_recambio_dialog)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)
        self.load_recambios()
    
    def load_recambios(self):
        filtro = self.filter_input.text()
        recambios = self.controller.get_recambios_by_name(filtro) if filtro else self.controller.get_all_recambios()

        self.table.setRowCount(len(recambios))

        for row, recambio in enumerate(recambios):
            self.table.setRowHeight(row, 40)

            # Verifica si recambio es un diccionario u objeto antes de acceder a sus valores
            if isinstance(recambio, dict):  
                valores = [recambio.get("id", ""), recambio.get("recambio", ""), recambio.get("cantidad", ""),
                        recambio.get("cantidad_minima", ""), recambio.get("stock_bajo", "")]
            elif isinstance(recambio, (list, tuple)):  
                valores = recambio[:5]  # Si es una lista/tupla, extrae los primeros 5 valores
            else:
                print(f"Error: tipo inesperado de recambio {type(recambio)}")  
                continue  

            for col, data in enumerate(valores):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Personalizar la columna "Stock" (columna 4)
                if col == 4:  
                    if data:  
                        item.setText("Bajo")  
                        item.setBackground(Qt.GlobalColor.red)  
                    else:  
                        item.setText("Correcto")  
                        item.setBackground(Qt.GlobalColor.green)  

                self.table.setItem(row, col, item)

            # Botones de acciones
            btn_layout = QHBoxLayout()

            btn_modify = self.create_button(
                "resources/images/modificacion.png", "Modificar", partial(self.modify_recambio, valores[0])
            )
            btn_layout.addWidget(btn_modify)

            btn_delete = self.create_button(
                "resources/images/borrar.png", "Borrar", partial(self.delete_recambio, valores[0])
            )
            btn_layout.addWidget(btn_delete)

            action_widget = QWidget()
            action_widget.setLayout(btn_layout)
            self.table.setCellWidget(row, 5, action_widget)


    def create_button(self, icon_path, tooltip, action):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(20, 20))
        button.setToolTip(tooltip)
        button.setFixedSize(27, 27)
        button.clicked.connect(action)
        return button

    def show_add_recambio_dialog(self):
        dialog = AddRecambioDialog()
        if dialog.exec():
            self.load_recambios()
    
    def modify_recambio(self, recambio_id):
        dialog = UpdateRecambioDialog(recambio_id)
        if dialog.exec():
            self.load_recambios()
    
    def delete_recambio(self, recambio_id):
        confirm = QMessageBox.question(
            self, "Confirmar", "¿Estás seguro de que quieres eliminar este recambio?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.controller.delete_recambio(recambio_id)
            self.load_recambios()