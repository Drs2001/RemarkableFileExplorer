import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QPushButton,QScrollBar, QListWidget, 
    QListWidgetItem, QHBoxLayout, QFileDialog,
    QLineEdit)
from PySide6.QtCore import Qt, QSize, QRunnable, Signal, QThreadPool, QObject
from PySide6.QtGui import QIcon
from Rm_Interaction.RMFileTree import RMFileTree
from gui.WaitingSpinner import WaitingSpinner

basedir = os.path.dirname(__file__)
assetsdir = 'assets'

class WorkerSignals(QObject):
    """
    Signals from a worker thread
    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)

class DownloadWorker(QRunnable):
    """
    A class used to represent a worker meant to download files

    ...

    Attributes
    ----------
    file : RMFile
        RMFile object that represents a document or folder on the tablet
    download_path : str
        The path we are downloading to
    signals : WorkerSignals
        Signals for our thread
    """
    def __init__(self, file, download_path):
        super().__init__()
        self.file = file
        self.download_path = download_path
        self.signals = WorkerSignals()

    def run(self):
        """Run the worker
        """
        self.file.download(self.download_path)
        self.signals.finished.emit()

class BackupWorker(QRunnable):
    """
    A class used to represent a worker meant to backup the tablet

    ...

    Attributes
    ----------
    fileTree : RMFileTree
        RMFileTree object that represents the RM file system
    download_path : str
        The path we are downloading to
    signals : WorkerSignals
        Signals for our thread
    """
    def __init__(self, fileTree, download_path):
        super().__init__()
        self.fileTree = fileTree
        self.download_path = download_path
        self.signals = WorkerSignals()

    def run(self):
        """Run the worker
        """
        self.fileTree.backup_tablet(self.download_path)
        self.signals.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__searchLength = 0
        self.__downloadPath = str(Path.home() / 'Downloads')
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()

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
        btn.setIcon(QIcon(os.path.join(basedir, assetsdir, 'arrow-left.svg')))
        btn.setFixedSize(QSize(30, 30))
        btn.clicked.connect(self.go_back)
        top_bar.addWidget(btn)

        # File Dialog Button
        btn = QPushButton()
        btn.setIcon(QIcon(os.path.join(basedir, assetsdir, 'folder.png')))
        btn.setFixedSize(QSize(30, 30))
        btn.clicked.connect(self.open_file_dialog)
        top_bar.addWidget(btn)

        top_bar.addStretch()

        # Add Search bar
        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.search_Files)
        top_bar.addWidget(self.search_bar)

        top_bar.addStretch()

        # Add the top bar to the layout
        layout.addLayout(top_bar)

        # Add the Remarkable file directory to the layout
        layout.addWidget(self.list_widget)

        # create widgets for the top of the screen
        bottom_bar = QHBoxLayout()

        btn = QPushButton("Download Selected")
        btn.clicked.connect(self.download_selected)
        bottom_bar.addWidget(btn)

        btn = QPushButton("Backup Tablet")
        btn.clicked.connect(self.backup_tablet)
        bottom_bar.addWidget(btn)

        layout.addLayout(bottom_bar)

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
            icon = os.path.join(basedir, assetsdir, 'folder.png')
            if file.get_type() == "DocumentType":
                icon = os.path.join(basedir, assetsdir, 'document.png')
            
            item.setIcon(QIcon(icon))
            self.list_widget.addItem(item)

    def search_Files(self):
        self.clear_list()
        if self.search_bar.text() == "":
            self.fileTree.clear_search()
            self.clear_list()
            self.update_list(self.fileTree.get_current_dir())
        else:
            # For the first increase we want to populate the search results so we do a full search
            if len(self.search_bar.text()) == 1 and not self.__searchLength > len(self.search_bar.text()):
                self.clear_list()
                self.update_list(self.fileTree.full_search_docs(self.search_bar.text()))
            # For every new character added to the search from the first we want to search the current search results to save time
            elif len(self.search_bar.text()) > self.__searchLength:
                self.clear_list()
                self.update_list(self.fileTree.half_search_docs(self.search_bar.text()))
        self.__searchLength = len(self.search_bar.text())
    
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
            # Setup the download spinner
            self.waiting_spinner = WaitingSpinner("Downloading...")
            self.waiting_spinner.show()

            # Disable the main window
            self.setDisabled(True)

            # Get the file and start the worker for download
            file = selected_items[0].data(Qt.ItemDataRole.UserRole)
            worker = DownloadWorker(file, self.__downloadPath)
            worker.signals.finished.connect(self.on_download_finished)
            self.threadpool.start(worker)

    def backup_tablet(self):
        """Downloads the entire tablet
        """
        # Setup the download spinner
        self.waiting_spinner = WaitingSpinner("Downloading...")
        self.waiting_spinner.show()

        # Disable the main window
        self.setDisabled(True)

        # Get the file and start the worker for download
        worker = BackupWorker(self.fileTree, self.__downloadPath)
        worker.signals.finished.connect(self.on_download_finished)
        self.threadpool.start(worker)
    
    def on_download_finished(self):
        """Closes the download spinner and reinables the window once the download has finished
        """
        self.waiting_spinner.close()
        self.waiting_spinner.deleteLater()
        self.setDisabled(False)

    def open_file_dialog(self):
        """Opens the file dialog to allow the user to select a downloads folder
        """
        dlg = QFileDialog(self)
        dlg.setDirectory(self.__downloadPath)
        self.__downloadPath = dlg.getExistingDirectory(self, "Select a Directory")
