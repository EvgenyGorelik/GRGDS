from PySide6.QtWidgets import QMainWindow
from gui.central_widget import CentralWidget
from gui.menu_bar import GuiMenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        menubar = GuiMenuBar(self)
        self.setMenuBar(menubar)
        widget = CentralWidget()
        self.setCentralWidget(widget)