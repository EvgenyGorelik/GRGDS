from PySide6.QtWidgets import QMenuBar, QFileDialog
from PySide6.QtGui import QAction

import os

class GuiMenuBar(QMenuBar):
    def __init__(self, parent, main_widget):
        super(GuiMenuBar, self).__init__(parent)

        self.main_widget = main_widget
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

        self.selected_files = None

    def newAction_clicked(self):
        dialog = QFileDialog(filter="Reflection Data File (*.hkl)")
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.exec()
        self.selected_files = dialog.selectedFiles()
        self.main_widget.file_list.clear()
        for f in self.get_file_list():
            self.main_widget.file_list.addItem(f)

    def get_file_list(self):
        return [os.path.basename(p) for p in self.selected_files]

    
    def exitAction_clicked(self):
        exit()