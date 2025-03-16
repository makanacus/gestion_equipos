import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from views.add_equipo_dialog import AddEquipoDialog  # Importamos el diálogo para agregar equipo
from views.update_equipo_dialog import UpdateEquipoDialog  # Importamos el diálogo para agregar equipo
from models.equipo_model import EquipoModel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Equipos")
        self.setGeometry(100, 100, 800, 600)
        
        self.equipo_model = EquipoModel()
        
        layout = QVBoxLayout()
        
        # Filtro por planta
        self.filter_layout = QHBoxLayout()
        self.planta_filter = QComboBox()
        self.planta_filter.addItem("Todas")
        self.planta_filter.addItems(self.get_ubicaciones())
        self.planta_filter.currentTextChanged.connect(self.load_equipos)
        self.filter_layout.addWidget(self.planta_filter)
        layout.addLayout(self.filter_layout)
        
        # Tabla de equipos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Equipo", "Modelo", "Ubicación", "Estado", "Acciones"])
        
        # Hacer que la tabla ocupe todo el ancho
        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Deshabilitar edición de celdas
        
        layout.addWidget(self.table)
        
        # Botón para agregar equipo
        self.add_button = QPushButton("Agregar Equipo")
        self.add_button.clicked.connect(self.show_add_equipo_dialog)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)
        self.load_equipos()
    
    def get_ubicaciones(self):
        equipos = self.equipo_model.get_all()
        return sorted(set(equipo[3] for equipo in equipos))  # Ubicación está en la posición 3
    
    def load_equipos(self):
        filtro = self.planta_filter.currentText()
        equipos = self.equipo_model.get_by_ubicacion(filtro) if filtro != "Todas" else self.equipo_model.get_all()
        
        self.table.setRowCount(len(equipos))  # Aseguramos que el número de filas sea correcto
        
        # Ajustamos la altura de todas las filas después de haber configurado el número de filas
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 40)  # Ajusta la altura de cada fila, por ejemplo, a 40 píxeles
        
        for row, equipo in enumerate(equipos):
            for col, data in enumerate(equipo[:5]):  # Mostrar datos en columnas
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar contenido de la celda
                self.table.setItem(row, col, item)
            
            # Botones de acción (siempre visibles)
            btn_layout = QHBoxLayout()
            
            icon_repuestos = QIcon("resources/images/recambios.png")  # Asegúrate de tener los iconos adecuados
            btn_repuestos = QPushButton()
            btn_repuestos.setIcon(icon_repuestos)
            btn_repuestos.setIconSize(QSize(20, 20))
            btn_repuestos.setToolTip("Repuestos")
            btn_repuestos.setFixedSize(27, 27)
            btn_repuestos.clicked.connect(lambda _, eq_id=equipo[0]: self.show_repuestos(eq_id))
            btn_layout.addWidget(btn_repuestos)
            
            icon_mantenimiento = QIcon("resources/images/mantenimiento.png")
            btn_mantenimiento = QPushButton()
            btn_mantenimiento.setIcon(icon_mantenimiento)
            btn_mantenimiento.setIconSize(QSize(20, 20))
            btn_mantenimiento.setToolTip("Mantenimiento")
            btn_mantenimiento.setFixedSize(27, 27)
            btn_mantenimiento.clicked.connect(lambda _, eq_id=equipo[0]: self.show_mantenimiento(eq_id))
            btn_layout.addWidget(btn_mantenimiento)
            
            icon_modify = QIcon("resources/images/modificacion.png")
            btn_modify = QPushButton()
            btn_modify.setIcon(icon_modify)
            btn_modify.setIconSize(QSize(20, 20))
            btn_modify.setToolTip("Modificar")
            btn_modify.setFixedSize(27, 27)
            btn_modify.clicked.connect(lambda _, eq_id=equipo[0]: self.modify_equipo(eq_id))
            btn_layout.addWidget(btn_modify)
            
            icon_delete = QIcon("resources/images/borrar.png")
            btn_delete = QPushButton()
            btn_delete.setIcon(icon_delete)
            btn_delete.setIconSize(QSize(20, 20))
            btn_delete.setToolTip("Borrar")
            btn_delete.setFixedSize(27, 27)
            btn_delete.clicked.connect(lambda _, eq_id=equipo[0]: self.delete_equipo(eq_id))
            btn_layout.addWidget(btn_delete)
            
            # Agregar los botones de acción a la tabla
            action_widget = QWidget()
            action_widget.setLayout(btn_layout)
            self.table.setCellWidget(row, 5, action_widget)

    def show_add_equipo_dialog(self):
        dialog = AddEquipoDialog()
        if dialog.exec():  # Si el usuario acepta el diálogo
            id = dialog.id_input.text()
            equipo = dialog.equipo_input.text()
            modelo = dialog.modelo_input.text()
            ubicacion = dialog.ubicacion_input.currentText()  # ✅ Obtiene la ubicación correctamente
            estado = dialog.estado_input.currentText()  # ✅ Obtiene el estado correctamente

            self.equipo_model.create(id, equipo, modelo, ubicacion, estado)
            self.load_equipos()  # Recargar la tabla de equipos

    
    def show_repuestos(self, equipo_id):
        print(f"Mostrar repuestos del equipo {equipo_id}")
    
    def show_mantenimiento(self, equipo_id):
        print(f"Mostrar mantenimiento del equipo {equipo_id}")
    
    def modify_equipo(self, equipo_id):
        equipo_data = self.equipo_model.get_by_id(equipo_id)
        if equipo_data:
            equipo_dict = {
                'id': str(equipo_data[0]),  # ✅ Incluir el ID correctamente
                'equipo': equipo_data[1],  # Nombre del equipo
                'modelo': equipo_data[2],  # Modelo
                'ubicacion': equipo_data[3],  # Ubicación
                'estado': equipo_data[4]  # Estado
            }
            dialog = UpdateEquipoDialog(equipo_id, equipo_dict, self.equipo_model)
            if dialog.exec():
                self.load_equipos()  # Recargar la tabla tras modificar el equipo


    
    def delete_equipo(self, equipo_id):
        print(f"Eliminar equipo {equipo_id}")
        self.equipo_model.delete(equipo_id)
        self.load_equipos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
