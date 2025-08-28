import os
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QByteArray
from PySide6 import QtGui

basedir = os.path.dirname(__file__)
assetsdir = 'assets'

class WaitingSpinner(QWidget):
    """
    Custom waiting spinner widget

    ...

    Attributes
    ----------
    title : str
        The title of the window
    """
    def __init__(self, title, parent=None):
        QWidget.__init__(self, parent)

        # Load the file into a QMovie
        self.movie = QtGui.QMovie(os.path.join(basedir, assetsdir, 'waiting-spinner.gif'), QByteArray(), self)

        self.setWindowTitle(title)

        self.movie_screen = QLabel()

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()