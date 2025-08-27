import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QPushButton,QScrollBar, QListWidget, 
    QListWidgetItem, QHBoxLayout, QFileDialog)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from RMFileTree import RMFileTree

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__downloadPath = str(Path.home() / 'Downloads')

        self.setWindowTitle("Remarkable File Explorer")
        window = QWidget()
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.navigate)

        # Initialize the root directory
        self.fileTree = RMFileTree()
        self.update_list(self.fileTree.get_current_dir())

        # create scrollbar
        scroll_bar = QScrollBar()
        scroll_bar.setStyleSheet("background : gray;")
        self.list_widget.setVerticalScrollBar(scroll_bar)

        # create widgets for the top of the screen
        top_bar = QHBoxLayout()

        # Back Button
        btn = QPushButton()
        btn.setIcon(QIcon('arrow-left.svg'))
        btn.setFixedSize(QSize(30, 30))
        btn.clicked.connect(self.go_back)
        top_bar.addWidget(btn)

        # File Dialog Button
        btn = QPushButton()
        btn.setIcon(QIcon('folder.png'))
        btn.setFixedSize(QSize(30, 30))
        btn.clicked.connect(self.open_file_dialog)
        top_bar.addWidget(btn)

        top_bar.addStretch()

        # Add the top bar to the layout
        layout.addLayout(top_bar)

        # Add the Remarkable file directory to the layout
        layout.addWidget(self.list_widget)

        btn = QPushButton("Download")
        btn.clicked.connect(self.download_selected)
        layout.addWidget(btn)

        window.setLayout(layout)
        self.setCentralWidget(window)
    
    def clear_list(self):
        """Clears the directory list
        """
        self.list_widget.clear()

    def update_list(self, dir):
        """Updates the current directory to the one passed in

        Parameters
        ----------
        dir : list(RMFiles)
            The directory to update the list to
        """
        for file in dir:
            item = QListWidgetItem(file.get_name())
            item.setData(Qt.ItemDataRole.UserRole, file)
            icon = "folder.png"
            if file.get_type() == "DocumentType":
                icon = "document.png"
            
            item.setIcon(QIcon(icon))
            self.list_widget.addItem(item)
    
    def navigate(self):
        """Navigates to the new directory of the folder double clicked,
        does nothing if the file clicked isnt of type 'CollectionType'
        """
        file = self.list_widget.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
        if file.get_type() == "CollectionType":
            self.clear_list()
            new_dir = file.get_children()
            self.fileTree.update_current_dir(new_dir)
            self.update_list(new_dir)
    
    def go_back(self):
        """Goes back to the previous directory
        """
        self.fileTree.back_to_previous()
        self.clear_list()
        self.update_list(self.fileTree.get_current_dir())

    def download_selected(self):
        """Downloads the selected document, or the entire folder and its subfolders
        of a selected folder.
        """
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) > 0:
            file = selected_items[0].data(Qt.ItemDataRole.UserRole)
            file.download(self.__downloadPath)

    def open_file_dialog(self):
        """Opens the file dialog to allow the user to select a downloads folder
        """
        dlg = QFileDialog(self)
        dlg.setDirectory(self.__downloadPath)
        self.__downloadPath = dlg.getExistingDirectory(self, "Select a Directory")
