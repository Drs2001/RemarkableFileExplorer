import sys
from PySide6.QtWidgets import QApplication
from gui.GUI import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
