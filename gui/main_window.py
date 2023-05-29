from PySide6.QtWidgets import QMainWindow
from gui.central_widget import CentralWidget
from gui.menu_bar import GuiMenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = CentralWidget()
        self.setCentralWidget(widget)
        menubar = GuiMenuBar(self, widget)
        self.setMenuBar(menubar)