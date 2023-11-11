from PySide6.QtWidgets import QLineEdit, QMenu

class CustomLineEdit(QLineEdit):
    """
    This method is used to create a custom context menu when a right-click event occurs.
    It creates a new QMenu, adds the standard context menu actions to it, and applies a custom style sheet.
    The menu is then displayed at the position of the right-click event.

    :param event: The right-click event that triggers the context menu.
    """
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