import socket
import struct
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

class WorkerThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, cliente, archivo_seleccionado):
        super().__init__()
        self.cliente = cliente
        self.archivo_seleccionado = archivo_seleccionado

    def run(self):
        conn = self.cliente.Conectar()
        if conn:
            self.progress.emit("Conectado al broker")
            self.cliente.EnviarArchivo(conn, "video_recibido.mp4")
            self.progress.emit("Archivo enviado, esperando procesamiento...")
            if self.cliente.RecibirArchivo(conn):
                self.progress.emit("Video procesado recibido exitosamente")
                self.finished.emit()
            else:
                self.error.emit("Error al recibir el archivo procesado")
        else:
            self.error.emit("Error al conectar con el broker")

class Cliente:
    def __init__(self):
        self.nombre = "Cliente"
        self.host = "localhost"
        self.port = 5000
        self.archivo = None

    def Conectar(self):
        try:
            s = socket.create_connection((self.host, self.port))
            return s
        except socket.error as e:
            return None
    
    def EnviarArchivo(self, conn, nombre_destino):
        try:
            with open(self.archivo, "rb") as f:
                data = f.read()
                file_size = struct.pack("!I", len(data))
                file_name = nombre_destino.encode()
                file_name_size = struct.pack("!I", len(file_name))
                conn.sendall(file_name_size + file_name + file_size + data)
            return True
        except Exception:
            return False

    def RecibirArchivo(self, conn):
        try:
            file_name_size = conn.recv(4)
            file_name_size = struct.unpack("!I", file_name_size)[0]
            file_name = conn.recv(file_name_size).decode()
            file_size = conn.recv(4)
            file_size = struct.unpack("!I", file_size)[0]
            data = b''
            while len(data) < file_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
            with open(file_name, "wb") as f:
                f.write(data)
                self.video = f.name
            return True
        except Exception:
            self.video = None
            return False

class ClienteGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cliente = Cliente()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cliente de Procesamiento de Video')
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QProgressBar {
                border: 2px solid #2196F3;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Título
        title = QLabel('Sistema de Procesamiento de Video')
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Botón para seleccionar archivo
        self.select_button = QPushButton('Seleccionar Video')
        self.select_button.clicked.connect(self.selectFile)
        layout.addWidget(self.select_button)

        # Etiqueta para mostrar archivo seleccionado
        self.file_label = QLabel('Ningún archivo seleccionado')
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)

        # Botón para procesar
        self.process_button = QPushButton('Procesar Video')
        self.process_button.clicked.connect(self.processVideo)
        self.process_button.setEnabled(False)
        layout.addWidget(self.process_button)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Estado
        self.status_label = QLabel('Esperando archivo...')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def selectFile(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if file_name:
            self.cliente.archivo = file_name
            self.file_label.setText(f"Archivo: {file_name.split('/')[-1]}")
            self.process_button.setEnabled(True)
            self.status_label.setText('Archivo seleccionado. Listo para procesar.')

    def processVideo(self):
        self.select_button.setEnabled(False)
        self.process_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText('Iniciando procesamiento...')

        self.worker = WorkerThread(self.cliente, self.cliente.archivo)
        self.worker.progress.connect(self.updateProgress)
        self.worker.finished.connect(self.processingComplete)
        self.worker.error.connect(self.processingError)
        self.worker.start()

    def updateProgress(self, message):
        self.status_label.setText(message)
        current = self.progress_bar.value()
        self.progress_bar.setValue(min(current + 30, 90))

    def processingComplete(self):
        self.progress_bar.setValue(100)
        self.status_label.setText('¡Procesamiento completado!')
        self.select_button.setEnabled(True)
        self.process_button.setEnabled(True)

    def processingError(self, error_message):
        self.status_label.setText(f'Error: {error_message}')
        self.progress_bar.setValue(0)
        self.select_button.setEnabled(True)
        self.process_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ClienteGUI()
    gui.show()
    sys.exit(app.exec())