"""PyQt5 Application"""

import sys

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from Coordinate import Coordinate, hashmark, yardline

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_axis_off()
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        img = plt.imread('ui/field.png')
        sc.axes.imshow(img)

        FIELD_SIZE = (889, 397)
        coord = Coordinate(4, yardline.A45, 0, hashmark.FH)
        sc.axes.plot(coord.get_x(FIELD_SIZE[0]), coord.get_y(FIELD_SIZE[1]), 'rx')
        # sc.axes.plot(300, 100, 'rx')
        # sc.axes.plot(500, 100, 'gx')
        # sc.axes.plot(300, 300, 'bx')
        # sc.axes.plot(500, 300, 'yx')
        self.setCentralWidget(sc)

        self.show()

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()