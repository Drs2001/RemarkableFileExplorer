from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QPushButton,QScrollBar, QListWidget, 
    QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from RMFileTree import RMFileTree

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

    def download_selected(self):
        """Downloads the selected document, or the entire folder and its subfolders
        of a selected folder.
        """
        print(self.list_widget.selectedItems()[0].data(Qt.ItemDataRole.UserRole))
        print(Qt.ItemDataRole.UserRole)
