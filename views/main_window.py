import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from views.equipos_view import EquiposView  # Importamos la vista de Equipos

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Equipos y Recambios")
        self.setGeometry(100, 100, 900, 600)

        # Crear el widget de pestañas
        self.tabs = QTabWidget()

        # Crear pestañas vacías
        self.tab_equipos = EquiposView() # Ahora usamos la vista independiente
        self.tab_recambios = QWidget() # Vacía por ahora

        # Agregar pestañas al widget
        self.tabs.addTab(self.tab_equipos, "Equipos")
        self.tabs.addTab(self.tab_recambios, "Recambios")

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
