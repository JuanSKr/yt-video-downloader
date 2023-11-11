from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QWidget, QDialog
)
from PySide6.QtGui import QAction, QKeySequence
import Downloader
import re
import gettext


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
        self.resize(800, 100)

        
        layout_vertical = QVBoxLayout()
        layout_downloader = QFormLayout()

        principal_component = QWidget()
        principal_component.setLayout(layout_vertical)

        self.setCentralWidget(principal_component)

        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Settings")

        self.menu_path = QAction("&Set path", self)
        self.menu_path.setShortcut(QKeySequence("Ctrl+P"))
        self.menu_path.triggered.connect(self.show_popup)

        self.set_language = QAction("&Language", self)
        self.set_language.setShortcut(QKeySequence("Ctrl+L"))
        self.set_language.triggered.connect(self.change_language)

        menu.addAction(self.menu_path)
        menu.addAction(self.set_language)

        self.language = 'en'
        self.translator = gettext.translation('base', localedir='locales', languages=[self.language], fallback=True)
        self.translator.install()

        self.downloader = Downloader.Downloader()

        self.path = "Empty"

        self.url = QLineEdit()
        self.url.setPlaceholderText("Enter the URL to download")
        self.url.setObjectName("url")

        self.download_mp4 = QPushButton("Download as MP4")
        self.download_mp4.setObjectName("downloadVideo")
        self.download_mp4.clicked.connect(self.download_video)

        self.download_mp3 = QPushButton("Download as MP3")
        self.download_mp3.setObjectName("downloadAudio")
        self.download_mp3.clicked.connect(self.download_audio)

        self.defined_path = QLabel("")
        self.label_path()

        self.download_status = QLabel("")

        layout_downloader.addRow(self.url)
        layout_downloader.addRow(self.download_mp4)
        layout_downloader.addRow(self.download_mp3)
        layout_downloader.addRow(self.defined_path)
        layout_downloader.addRow(self.download_status)

        layout_vertical.addLayout(layout_downloader)

    def download_video(self):
        url = self.url.text()
        if self.validate_youtube_short_url(url) or self.validate_youtube_full_url(url):
            self.download_status.setText("Downloading...")
            try:
                self.downloader.download_video(url, self.path)
                self.download_status.setText("Download completed")
                self.download_status.setStyleSheet("color: green")
            except:
                self.download_status.setText("Download failed")
                self.download_status.setStyleSheet("color: red")
        else:
            self.download_status.setText("Invalid URL format")
            self.download_status.setStyleSheet("color: red")

    def download_audio(self):
        url = self.url.text()
        if self.validate_youtube_short_url(url) or self.validate_youtube_full_url(url):
            self.download_status.setText("Downloading...")
            try:
                self.downloader.download_audio(url, self.path)
                self.download_status.setText("Download completed")
                self.download_status.setStyleSheet("color: green")
            except:
                self.download_status.setText("Download failed")
                self.download_status.setStyleSheet("color: red")
        else:
            self.download_status.setText("Invalid URL format")
            self.download_status.setStyleSheet("color: red")

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

    def validate_youtube_short_url(self, url):
        pattern = r'^https://youtu\.be/.*$'
        if re.match(pattern, url):
            return True
        else:
            return False

    def validate_youtube_full_url(self, url):
        pattern = r'^https://www\.youtube\.com/.*$'
        if re.match(pattern, url):
            return True
        else:
            return False

    def change_language(self):
        if self.language == 'en':
            self.language = 'es'
        else:
            self.language = 'en'
        self.translator = gettext.translation('base', localedir='locales', languages=[self.language], fallback=True)
        self.translator.install()
        self.update_ui()

    def update_ui(self):
        if self.language == 'en':
            self.setWindowTitle("YouTube Downloader")
            self.download_mp4.setText("Download as MP4")
            self.download_mp3.setText("Download as MP3")
            self.download_status.setText("")
            self.defined_path.setText(f"Current Path: {self.path}")
            self.url.setPlaceholderText("Enter the URL to download")
        else:
            self.setWindowTitle("Descargador de vídeos de YouTube")
            self.download_mp4.setText("Descargar como MP4")
            self.download_mp3.setText("Descargar como MP3")
            self.download_status.setText("")
            self.defined_path.setText(f"Ruta actual: {self.path}")
            self.url.setPlaceholderText("Ingrese la URL a descargar")


if __name__ == "__main__":
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    app.exec()
