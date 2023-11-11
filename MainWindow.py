from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, \
    QComboBox, QHBoxLayout, QWidget, QDialog
from PySide6.QtGui import QAction, QKeySequence
import Downloader
import re


class PopupPath(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle("Download path")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter the path")

        self.button = QPushButton("Set path")
        self.button.clicked.connect(mainWindow.set_path)

        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.resize(800, 420)

        layout_vertical = QVBoxLayout()
        layout_downloader = QFormLayout()

        principal_component = QWidget()
        principal_component.setLayout(layout_vertical)

        self.setCentralWidget(principal_component)

        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Settings")

        accion = QAction("&Set path", self)
        accion.setShortcut(QKeySequence("Ctrl+P"))
        accion.triggered.connect(self.show_popup)

        menu.addAction(accion)

        self.downloader = Downloader.Downloader()

        self.path = "Empty"

        self.url = QLineEdit()
        self.url.setPlaceholderText("Enter the URL to download")
        self.url.setObjectName("url")

        self.download_mp4 = QPushButton("Download as MP4")
        self.download_mp4.setObjectName("downloadMp4")
        self.download_mp4.clicked.connect(self.print_path)

        self.download_mp3 = QPushButton("Download as MP3")
        self.download_mp3.setObjectName("downloadMp3")
        self.download_mp3.clicked.connect(self.print_path)

        self.defined_path = QLabel("")
        self.label_path()

        layout_downloader.addRow(self.url)
        layout_downloader.addRow(self.download_mp4)
        layout_downloader.addRow(self.download_mp3)
        layout_downloader.addRow(self.defined_path)

        layout_vertical.addLayout(layout_downloader)

    def download_video(self):
        url = self.url.text()
        self.downloader.download_video(url, self.path)

    def show_popup(self):
        self.dialog = PopupPath(self)
        self.dialog.show()

    def set_path(self):
        path = self.dialog.lineEdit.text()
        if self.validate_path(path):
            self.path = path
            self.label_path()
            self.dialog.close()
        else:
            print("Invalid path format.")

    def print_path(self):
        print(self.path)

    def label_path(self):
        self.defined_path.setText(f"Current Path: {self.path}")

    def validate_path(self, path):
        pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
        if re.match(pattern, path):
            return True
        else:
            return False


if __name__ == "__main__":
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    app.exec()
