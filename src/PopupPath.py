from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from CustomLineEdit import CustomLineEdit

class PopupPath(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle("Download path")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.lineEdit = CustomLineEdit()
        self.lineEdit.setPlaceholderText("Enter the path")
        self.lineEdit.setObjectName("path")

        self.path_button = QPushButton("Set path")
        self.path_button.clicked.connect(mainWindow.set_path)
        self.path_button.setObjectName("setPath")

        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.path_button)