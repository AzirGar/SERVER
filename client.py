import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 400, 200)

        self.btn_cargar = QPushButton("Cargar Archivo", self)
        self.btn_cargar.clicked.connect(self.upload_file)
        self.btn_cargar.setGeometry(150, 50, 100, 30)

    def upload_file(self):
        file_dialog = QFileDialog()
        filename = file_dialog.getOpenFileName(self, 'Seleccionar archivo')[0]
        if filename:
            files = {'file': open(filename, 'rb')}
            response = requests.post('http://localhost:5000/upload', files=files)
            if response.status_code == 200:
                print("Archivo cargado exitosamente.")
            else:
                print("Error al cargar el archivo.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
