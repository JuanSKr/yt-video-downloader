from PySide6.QtWidgets import QLineEdit, QMenu

class CustomLineEdit(QLineEdit):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        actions = self.createStandardContextMenu().actions()
        for action in actions:
            menu.addAction(action)
        menu.setStyleSheet("""
            QMenu {
                background-color: #4B4B4B;
                color: #FFFFFF;
                border: 1px solid #555;
                font-family: "Spendthrift";
            }
            QMenu::item:selected {
                background-color: #C4302B;
            }
        """)
        menu.exec_(event.globalPos())