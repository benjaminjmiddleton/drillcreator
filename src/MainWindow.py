from os.path import expanduser

# matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# qt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QSettings, QFileInfo, QPoint

# drillcreator
from Coordinate import Coordinate, hashmark, yardline
from Show import Show

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_axis_off()
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    FIELD_SIZE = (886, 389) # dimensions of ui/field.png

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        img = plt.imread('ui/field.png')
        sc.axes.imshow(img)

        # PLOT TEST POINTS
        # coord = Coordinate(4, yardline.A45, 0, hashmark.BSL)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bx')

        # coord = Coordinate(4, yardline.A45, 0, hashmark.BH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(4, yardline.A45, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'yx')

        # coord = Coordinate(4, yardline.A45, 0, hashmark.FSL)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(-16, yardline.A_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(-16, yardline.B_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(0, yardline.A_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(0, yardline.B_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # sc.axes.plot(300, 100, 'rx')
        # sc.axes.plot(500, 100, 'gx')
        # sc.axes.plot(300, 300, 'bx')
        # sc.axes.plot(500, 300, 'yx')
        
        self.setCentralWidget(sc)

        self.menuNew.actions()[0].triggered.connect(self.new_band)
        self.menuNew.actions()[0].triggered.connect(self.new_show)

        self.menuAdd_Drillset.actions()[0].triggered.connect(self.add_set_from_image)
        self.menuAdd_Drillset.actions()[1].triggered.connect(self.add_empty_set)
        self.menuAdd_Drillset.actions()[2].triggered.connect(self.add_copy_of_current_set)

        self.actionSave.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.save_as)

        self.read_settings()

        self.show()
    
    def __del__(self):
        self.save_settings()

    def read_settings(self):
        settings = QSettings("University of Cincinnati", "drillcreator")

        pos = settings.value("MainWindow/pos", defaultValue=QPoint(0,0))
        size = settings.value("MainWindow/size", defaultValue=self.FIELD_SIZE)
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])

        self.last_dir = settings.value("MainWindow/last_dir", defaultValue=expanduser("~"))

        self.loaded_show = settings.value("MainWindow/loaded_show", defaultValue="../data/band1.pf")
    
    def save_settings(self):
        settings = QSettings("University of Cincinnati", "drillcreator")

        settings.beginGroup("MainWindow")
        pos = self.frameGeometry().topLeft()
        settings.setValue("pos", self.frameGeometry().topLeft())
        settings.setValue("size", (self.frameGeometry().width(), self.frameGeometry().height()))
        settings.setValue("last_dir", self.last_dir)
        settings.setValue("loaded_show", self.loaded_show)
        settings.endGroup()

    def new_show(self):
        file_tuple = QFileDialog.getOpenFileName(self, "Open Performer File", self.last_dir, "Performer Files (*.pf)")
        if file_tuple[0] != '':
            self.last_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            self.loaded_show = Show(Show.load_performers(file_tuple[0]))

    def new_band(self):
        pass

    def open(self):
        print('open')
    
    def add_set_from_image(self):
        print('from image')

    def add_empty_set(self):
        print('empty')

    def add_copy_of_current_set(self):
        print('copy')
    
    def save(self):
        print('save')
    
    def save_as(self):
        print('save')

# TODO this file
# serialize and deserialize self.loaded_show and .pf files (save(), save_as(), open()) - this will also mean rewriting Show.load_performers().
# add_copy_of_current_set (need sidebar first)

# TODO major features
# sidebar that allows stepping through counts/sets and displays drillset info
# allow editing of a performer's co-ordinate in a drillset
# performer view (steps through counts/sets with a specific performer highlighted and flips the field view)
#
# add_set_from_image (this will integrate both the image converter and the drill solver. If the loaded show has a
# pre-existing drillset, we need to allocate the performers to the new shape using the drill solver.)

# TODO Status Bar
# There should be a status bar at the bottom of the main window that shows the latest/current functions being performed
# by the application. For example, when solving a particularly complex drill, a message will appear stating as much. Or
# if a file was just saved, that status bar will say "File saved as 'Fake Path To File'".
