from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from views.add_equipo_dialog import AddEquipoDialog
from views.update_equipo_dialog import UpdateEquipoDialog
from controllers.equipo_controller import EquipoController

class EquiposView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.controller = EquipoController()  # Usar el controlador en lugar del modelo
        
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
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.table)
        
        # Botón para agregar equipo
        self.add_button = QPushButton("Agregar Equipo")
        self.add_button.clicked.connect(self.show_add_equipo_dialog)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)
        self.load_equipos()
    
    def get_ubicaciones(self):
        equipos = self.controller.get_all_equipos()  # Usar el controlador
        return sorted(set(equipo[3] for equipo in equipos))
    
    def load_equipos(self):
        filtro = self.planta_filter.currentText()
        equipos = self.controller.get_equipos_by_ubicacion(filtro) if filtro != "Todas" else self.controller.get_all_equipos()
        
        self.table.setRowCount(len(equipos))
        
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 40)
        
        for row, equipo in enumerate(equipos):
            for col, data in enumerate(equipo[:5]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
            
            btn_layout = QHBoxLayout()
            
            btn_repuestos = self.create_button("resources/images/recambios.png", "Repuestos", lambda _, eq_id=equipo[0]: self.show_repuestos(eq_id))
            btn_layout.addWidget(btn_repuestos)
            
            btn_mantenimiento = self.create_button("resources/images/mantenimiento.png", "Mantenimiento", lambda _, eq_id=equipo[0]: self.show_mantenimiento(eq_id))
            btn_layout.addWidget(btn_mantenimiento)
            
            btn_modify = self.create_button("resources/images/modificacion.png", "Modificar", lambda _, eq_id=equipo[0]: self.modify_equipo(eq_id))
            btn_layout.addWidget(btn_modify)
            
            btn_delete = self.create_button("resources/images/borrar.png", "Borrar", lambda _, eq_id=equipo[0]: self.delete_equipo(eq_id))
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

    def show_add_equipo_dialog(self):
        dialog = AddEquipoDialog()
        if dialog.exec():
            id = dialog.id_input.text()
            equipo = dialog.equipo_input.text()
            modelo = dialog.modelo_input.text()
            ubicacion = dialog.ubicacion_input.currentText()
            estado = dialog.estado_input.currentText()
            self.controller.create_equipo(id, equipo, modelo, ubicacion, estado)  # Usar el controlador
            self.load_equipos()
    
    def show_repuestos(self, equipo_id):
        print(f"Mostrar repuestos del equipo {equipo_id}")
    
    def show_mantenimiento(self, equipo_id):
        print(f"Mostrar mantenimiento del equipo {equipo_id}")
    
    def modify_equipo(self, equipo_id):
        equipo_data = self.controller.get_equipo_by_id(equipo_id)  # Usar el controlador
        if equipo_data:
            equipo_dict = {
                'id': str(equipo_data[0]),
                'equipo': equipo_data[1],
                'modelo': equipo_data[2],
                'ubicacion': equipo_data[3],
                'estado': equipo_data[4]
            }
            dialog = UpdateEquipoDialog(equipo_id, equipo_dict, self.controller)  # Pasar el controlador
            if dialog.exec():
                self.load_equipos()
    
    def delete_equipo(self, equipo_id):
        print(f"Eliminar equipo {equipo_id}")
        self.controller.delete_equipo(equipo_id)  # Usar el controlador
        self.load_equipos()