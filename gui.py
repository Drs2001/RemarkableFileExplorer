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
        self.initialize_root_dir()

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
        self.list_widget.clear()

    def initialize_root_dir(self):
        dir = self.fileTree.get_base_dir()
        for file in dir:
            item = QListWidgetItem(file.get_name())
            item.setData(Qt.ItemDataRole.UserRole, file.get_id())
            icon = "folder.png"
            if file.get_type() == "DocumentType":
                icon = "document.png"
            
            item.setIcon(QIcon(icon))
            self.list_widget.addItem(item)

    def download_selected(self):
        print(self.list_widget.selectedItems()[0].data(Qt.ItemDataRole.UserRole))
        print(Qt.ItemDataRole.UserRole)
    
    def navigate(self):
        print("Working")
