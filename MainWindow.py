from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QWidget, QDialog
)
from PySide6.QtGui import QAction, QKeySequence, QPixmap
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
        self.resize(500, 300)

        # Define the layout of the main window
        layout_vertical = QVBoxLayout()
        # Define the layout of the downloader
        layout_downloader = QFormLayout()

        # Define the main component
        principal_component = QWidget()
        # Set the layout of the main component
        principal_component.setLayout(layout_vertical)
        principal_component.setObjectName("principalComponent")

        # Set the main component as the central widget
        self.setCentralWidget(principal_component)

        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Settings")

        # Define the menu bar actions and connect them to the functions (path)
        self.menu_path = QAction("&Set path", self)
        self.menu_path.setShortcut(QKeySequence("Ctrl+P"))
        self.menu_path.triggered.connect(self.show_popup)

        # Add the actions to the menu bar (path)
        menu.addAction(self.menu_path)

        # Define the downloader object
        self.downloader = Downloader.Downloader()

        # Define the path to Empty
        self.path = "Empty"

        # Define the components of the downloader (URL, Download as MP4, Download as MP3)
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
        self.defined_path.setStyleSheet("font-family: Spendthrift;")
        self.label_path()

        self.download_status = QLabel("")
        self.download_status.setStyleSheet("font-family: Spendthrift;")

        self.image_label = QLabel()
        self.pixmap = QPixmap('resources/logo.png')
        self.pixmap = self.pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.FastTransformation)

        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Add the components to the layout
        layout_downloader.addWidget(self.image_label)
        layout_downloader.addRow(self.url)
        layout_downloader.addRow(self.download_mp4)
        layout_downloader.addRow(self.download_mp3)
        layout_downloader.addRow(self.defined_path)
        layout_downloader.addRow(self.download_status)

        # Add the layout to the main layout
        layout_vertical.addLayout(layout_downloader)

    def download_video(self):
        """
        Downloads a YouTube video.

        This method retrieves the YouTube video URL from the user interface text input,
        validates the URL, and then attempts to download the video using the Downloader object.
        It updates the download status on the user interface.

        If the URL is valid and the download is successful, it displays "Download completed" in green.
        If the URL is valid but the download fails, it displays "Download failed" in red.
        If the URL is invalid, it displays "Invalid URL format" in red.
        """
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
        """
        Downloads the audio from a YouTube video.

        This method retrieves the YouTube video URL from the user interface text input,
        validates the URL, and then attempts to download the audio using the Downloader object.
        It updates the download status on the user interface.

        If the URL is valid and the download is successful, it displays "Download completed" in green.
        If the URL is valid but the download fails, it displays "Download failed" in red.
        If the URL is invalid, it displays "Invalid URL format" in red.
        """
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
        """
        Displays a popup for setting the download path.

        This method creates a new instance of the PopupPath class, passing the current instance of the MainWindow class.
        It then displays the popup to the user.
        """
        self.dialog = PopupPath(self)
        self.dialog.show()

    def set_path(self):
        """
        Sets the download path.

        This method retrieves the path from the dialog's text input,
        validates the path, and if valid, sets the path, updates the path label, and closes the dialog.
        If the path is invalid, it prints "Invalid path format." to the console.
        """
        path = self.dialog.lineEdit.text()
        if self.validate_path(path):
            self.path = path
            self.label_path()
            self.dialog.close()
        else:
            print("Invalid path format.")

    def label_path(self):
        """
        Updates the displayed download path.

        This method sets the text of the 'defined_path' label to display the current download path.
        """
        self.defined_path.setText(f"Current Path: {self.path}")

    def validate_path(self, path):
        """
        Validates a file path.

        This method checks if the provided path is a valid file path on Windows.
        It uses a regular expression to check if the path matches the pattern of a valid file path.

        :param path: The path to validate.

        :return True if the path is valid, False otherwise.
        """
        pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
        if re.match(pattern, path):
            return True
        else:
            return False

    def validate_youtube_short_url(self, url):
        """
        Validates a short YouTube URL.

        This method checks if the provided URL is a valid short YouTube URL.
        It uses a regular expression to check if the URL matches the pattern of a valid short YouTube URL.

        :param url: The URL to validate.

        :return True if the URL is valid, False otherwise.
        """
        pattern = r'^https://youtu\.be/.*$'
        if re.match(pattern, url):
            return True
        else:
            return False

    def validate_youtube_full_url(self, url):
        """
        Validates a full YouTube URL.

        This method checks if the provided URL is a valid full YouTube URL.
        It uses a regular expression to check if the URL matches the pattern of a valid full YouTube URL.

        :param url: The URL to validate.

        :return True if the URL is valid, False otherwise.
        """
        pattern = r'^https://www\.youtube\.com/.*$'
        if re.match(pattern, url):
            return True
        else:
            return False


if __name__ == "__main__":
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    with open("resources/styles.qss", "r") as style:
        app.setStyleSheet(style.read())
    app.exec()
