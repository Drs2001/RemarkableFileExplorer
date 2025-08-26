import sys
from PySide6.QtWidgets import QApplication
from RM_API import RM_API
from gui import MainWindow
from RMFileTree import RMFileTree


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    # file_tree = RMFileTree()
    # currentDir = file_tree.get_current_dir()
    # for file in currentDir:
    #     print(file.get_type())
