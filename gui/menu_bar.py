from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction

class GuiMenuBar(QMenuBar):
    def __init__(self, parent):
        super(GuiMenuBar, self).__init__(parent)
        fileMenu = self.addMenu("&File")
        editMenu = self.addMenu("&Edit")
        helpMenu = self.addMenu("&Help")

        
        self.newAction = QAction("&New", self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

        # Edit menu
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        # Help menu
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)


        self.newAction.triggered.connect(self.newAction_clicked)
        self.exitAction.triggered.connect(self.exitAction_clicked)

    def newAction_clicked(self):
        print("clicked")

    
    def exitAction_clicked(self):
        exit()