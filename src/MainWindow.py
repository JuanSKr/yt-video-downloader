from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QFormLayout, QPushButton, QLabel, QWidget, QFileDialog
)
from PySide6.QtGui import QAction, QKeySequence, QPixmap
import Downloader
import re
import webbrowser

from CustomLineEdit import CustomLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setFixedSize(520, 330)

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

        bar = self.menuBar()
        bar.setObjectName("menuBar")
        bar.setStyleSheet("font-family: Spendthrift; color: #FFFFFF; font-weight: bold;")
        settings = bar.addMenu("&Settings")
        settings.setStyleSheet("font-family: Spendthrift; color: #FFFFFF; font-weight: bold;")
        info = bar.addMenu("&Info")
        info.setStyleSheet("font-family: Spendthrift; color: #FFFFFF; font-weight: bold;")

        # Define the menu bar actions and connect them to the functions (path)
        self.menu_path = QAction("&Set path", self)
        self.menu_path.setShortcut(QKeySequence("Ctrl+P"))
        self.menu_path.triggered.connect(self.set_path)

        profile_action = QAction('GitHub &Profile', self)
        profile_action.triggered.connect(self.open_profile)

        # Create the 'GitHub Repository' menu item and connect it to the 'open_repository' method
        repo_action = QAction('GitHub &Repository', self)
        repo_action.triggered.connect(self.open_repository)

        # Add the actions to the menu bar
        settings.addAction(self.menu_path)
        info.addAction(profile_action)
        info.addAction(repo_action)

        # Define the downloader object
        self.downloader = Downloader.Downloader()

        # Define the path to Empty
        self.path = "Undefined"

        # Define the components of the downloader (URL, Download as MP4, Download as MP3)
        self.url = CustomLineEdit()
        self.url.setPlaceholderText("Enter the URL to download")
        self.url.setObjectName("url")

        # Define the download buttons
        self.download_mp4 = QPushButton("Download as MP4")
        self.download_mp4.setObjectName("downloadVideo")
        self.download_mp4.clicked.connect(self.download_video)

        self.download_mp3 = QPushButton("Download as MP3")
        self.download_mp3.setObjectName("downloadMp3")
        self.download_mp3.clicked.connect(self.download_as_mp3)

        self.download_wav = QPushButton("Download as WAV")
        self.download_wav.setObjectName("downloadWav")
        self.download_wav.clicked.connect(self.download_as_wav)

        # Define the path label
        self.defined_path = QLabel("")
        self.defined_path.setStyleSheet("font-family: Spendthrift; color: #FFFFFF; font-weight: bold;")
        self.label_path()

        # Define the download status label
        self.download_status = QLabel("")

        # Define the image label and the image to display
        self.image_label = QLabel()
        self.pixmap = QPixmap("../resources/logo.png")
        self.pixmap = self.pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.FastTransformation)

        # Set the image to the label and center it
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Add the components to the layout
        layout_downloader.addWidget(self.image_label)
        layout_downloader.addRow(self.url)
        layout_downloader.addRow(self.download_mp4)
        layout_downloader.addRow(self.download_mp3)
        layout_downloader.addRow(self.download_wav)
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
            try:
                self.downloader.download_video(url, self.path)
                self.download_status.setText("Download completed")
                self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #4dff4d")
            except:
                self.download_status.setText("Download failed")
                self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #ff8000")
        else:
            self.download_status.setText("Invalid URL format")
            self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #ff8000")

    def download_as_mp3(self):
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
            try:
                self.downloader.download_mp3(url, self.path)
                self.download_status.setText("Download completed")
                self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #4dff4d")
            except:
                self.download_status.setText("Download failed")
                self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #ff8000")
        else:
            self.download_status.setText("Invalid URL format")
            self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #ff8000")

    def download_as_wav(self):
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
            try:
                self.downloader.download_wav(url, self.path)
                self.download_status.setText("Download completed")
                self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #4dff4d")
            except:
                self.download_status.setText("Download failed")
                self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #ff8000")
        else:
            self.download_status.setText("Invalid URL format")
            self.download_status.setStyleSheet("font-family: Spendthrift; font-weight: bold; color: #ff8000")

    def set_path(self):
        """
        This method is used to set the download path for the YouTube videos.
        It opens a file dialog for the user to select an existing directory.
        After the path is selected, it updates the path label with the new path.
        """
        self.path = QFileDialog.getExistingDirectory(self, "Select a directory")
        self.label_path()

    def label_path(self):
        """
        Updates the displayed download path.

        This method sets the text of the 'defined_path' label to display the current download path.
        """
        if self.path is not None:
            self.defined_path.setText(f"Current Path: {self.path}")

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

    def open_profile(self):
        """
        This method is used to open the GitHub profile of the developer in the default web browser.
        It does not take any parameters and does not return any value.
        """
        webbrowser.open('https://github.com/JuanSKr')

    def open_repository(self):
        """
        This method is used to open the GitHub repository of the YouTube Downloader project in the default web browser.
        It does not take any parameters and does not return any value.
        """
        webbrowser.open('https://github.com/JuanSKr/yt-video-downloader')


if __name__ == "__main__":
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    with open("../resources/styles.qss", "r") as style:
        app.setStyleSheet(style.read())
    app.exec()
