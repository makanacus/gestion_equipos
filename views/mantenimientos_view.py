import textwrap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QAbstractItemView, QMessageBox, QDateEdit
)
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import QSize, Qt, QDate
from controllers.mantenimiento_controller import MantenimientoController
from functools import partial

class MantenimientosView(QWidget):
    def __init__(self, equipo_id):
        super().__init__()
        self.equipo_id = equipo_id
        self.controller = MantenimientoController()

        # Establecer tamaño y título de la ventana
        self.setGeometry(120, 120, 900, 600)
        self.setWindowTitle(f"Mantenimientos del Equipo {self.equipo_id}")  # Título con el ID del equipo
        
        layout = QVBoxLayout()
        
        # Filtro por rango de fechas
        filter_layout = QHBoxLayout()

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.setDate(QDate.currentDate().addDays(-30))  # Fecha predeterminada: 30 días atrás
        filter_layout.addWidget(self.date_from)

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.setDate(QDate.currentDate())  # Fecha predeterminada: Hoy
        filter_layout.addWidget(self.date_to)

        
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.load_mantenimientos)
        filter_layout.addWidget(self.search_button)
        
        layout.addLayout(filter_layout)
        
        # Tabla de mantenimientos
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Intervalo", "Próximo Mantenimiento", "Recambios Utilizados", "Descripción", "Acciones"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.table)

        # Botón "Agregar Mantenimiento"
        self.add_button = QPushButton("Agregar Mantenimiento")
        self.add_button.setIcon(QIcon("resources/images/agregar.png"))  # Icono del botón
        self.add_button.setIconSize(QSize(20, 20))
        self.add_button.setToolTip("Añadir un nuevo mantenimiento")
        self.add_button.clicked.connect(self.add_mantenimiento)

        layout.addWidget(self.add_button) 

        self.setLayout(layout)
        self.load_mantenimientos()

    def load_mantenimientos(self):
        date_from = self.date_from.date().toString("yyyy-MM-dd") if self.date_from.date().isValid() else None
        date_to = self.date_to.date().toString("yyyy-MM-dd") if self.date_to.date().isValid() else None

        mantenimientos = self.controller.obtener_mantenimientos_por_equipo(self.equipo_id)

        if date_from and date_to:
            mantenimientos = [m for m in mantenimientos if date_from <= m[2] <= date_to]

        self.table.setRowCount(len(mantenimientos))

        today = QDate.currentDate()  # Fecha actual
        last_row = len(mantenimientos) - 1  # Índice del último registro

        for row, mantenimiento in enumerate(mantenimientos):
            self.table.setRowHeight(row, 40)
            valores = [mantenimiento[0], mantenimiento[2], mantenimiento[3], mantenimiento[4], mantenimiento[5], mantenimiento[6]]

            for col, data in enumerate(valores):
                # Si el valor es None, "", o "null", dejar la celda vacía
                data = "" if data is None or str(data).strip().lower() == "null" or str(data).strip() == "" else str(data)

                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Si es la última fila y es la columna "Próximo Mantenimiento" (índice 3)
                if row == last_row and col == 3 and data:
                    proximo_mantenimiento = QDate.fromString(data, "yyyy-MM-dd")
                    dias_restantes = today.daysTo(proximo_mantenimiento)

                    if dias_restantes <= 7:  
                        item.setBackground(QColor(255, 0, 0))  # Rojo
                    else:
                        item.setBackground(QColor(0, 255, 0))  # Verde
                
                # Si es la columna "Descripción" (índice 5), agregar tooltip con texto formateado
                if col == 5 and data:
                    descripcion_formateada = textwrap.fill(data, width=50)  # Divide en líneas de 50 caracteres
                    item.setToolTip(descripcion_formateada)

                self.table.setItem(row, col, item)

            # Botones de acciones
            btn_layout = QHBoxLayout()

            # Solo mostrar el botón de "Modificar" en el último mantenimiento
            if row == last_row:
                btn_modify = self.create_button("resources/images/modificacion.png", "Modificar", partial(self.modify_mantenimiento, valores[0]))
                btn_layout.addWidget(btn_modify)

            btn_delete = self.create_button("resources/images/borrar.png", "Borrar", partial(self.delete_mantenimiento, valores[0]))
            btn_layout.addWidget(btn_delete)

            action_widget = QWidget()
            action_widget.setLayout(btn_layout)
            self.table.setCellWidget(row, 6, action_widget)
            
    def create_button(self, icon_path, tooltip, action):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(20, 20))
        button.setToolTip(tooltip)
        button.setFixedSize(27, 27)
        button.clicked.connect(action)
        return button
    
    def add_mantenimiento(self):
        """
        Método para agregar un nuevo mantenimiento.
        Aquí puedes abrir una nueva ventana o formulario para ingresar los datos.
        """
        QMessageBox.information(self, "Agregar", "Aquí irá la lógica para agregar un mantenimiento.")
    
    def modify_mantenimiento(self, mantenimiento_id):
        # Lógica para modificar el mantenimiento
        pass
    
    def delete_mantenimiento(self, mantenimiento_id):
        confirm = QMessageBox.question(
            self, "Confirmar", "¿Estás seguro de que quieres eliminar este mantenimiento?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.controller.eliminar_mantenimiento(mantenimiento_id)
            self.load_mantenimientos()