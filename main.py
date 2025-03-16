# main.py
import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow  # Importamos la clase MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  # Crear una instancia de MainWindow
    window.show()
    sys.exit(app.exec())  # Iniciar la aplicación PyQt6
