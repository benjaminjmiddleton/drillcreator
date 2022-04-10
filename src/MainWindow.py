from os.path import expanduser
import json

# matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# pyqt5
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QWidget, QSizePolicy, QDialog
from PyQt5.QtCore import QSettings, QFileInfo, QPoint, pyqtSignal

# drillcreator
from Coordinate import Coordinate, hashmark, yardline
from Show import Show
from NewBandDialog import NewBandDialog

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_axis_off()
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    FIELD_SIZE = (886, 389) # dimensions of ui/field.png
    active_set_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/MainWindow.ui', self)
        self.setWindowTitle("Drill Creator")

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        img = plt.imread('ui/field.png')
        sc.axes.imshow(img)

        navigation_box = QWidget()
        navigation_box.setMinimumSize(360, 50)
        uic.loadUi('ui/NavigationBox.ui', navigation_box)
        policy = QSizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Fixed)
        policy.setHorizontalPolicy(QSizePolicy.Expanding)
        navigation_box.setSizePolicy(policy)

        layout = QVBoxLayout()
        layout.addWidget(sc)
        layout.addWidget(navigation_box)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

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
        
        self.active_set_changed.connect(self.draw_active_set)

        self.menuNew.actions()[0].triggered.connect(self.new_band)
        self.menuNew.actions()[1].triggered.connect(self.new_show)

        self.menuAdd_Drillset.actions()[0].triggered.connect(self.add_set_from_image)
        self.menuAdd_Drillset.actions()[1].triggered.connect(self.add_empty_set)
        self.menuAdd_Drillset.actions()[2].triggered.connect(self.add_copy_of_current_set)

        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.save_as)

        navigation_box.leftArrowButton.clicked.connect(self.previous_set)
        navigation_box.rightArrowButton.clicked.connect(self.next_set)
        navigation_box.modeButton.clicked.connect(self.toggle_navigation_mode)
        navigation_box.informationButton.clicked.connect(self.show_active_set_information)

        self.read_settings()

        self.show()
    
    def closeEvent(self, event):
        self.save_settings()

    def read_settings(self):
        settings = QSettings("University of Cincinnati", "drillcreator")

        pos = settings.value("MainWindow/pos", defaultValue=QPoint(0,0))
        size = settings.value("MainWindow/size", defaultValue=self.FIELD_SIZE)
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])

        self.last_dir = settings.value("MainWindow/last_dir", defaultValue=expanduser("~"))

        self.loaded_show = settings.value("MainWindow/loaded_show", defaultValue=Show([]))

        self.active_set_changed.emit()
    
    def save_settings(self):
        settings = QSettings("University of Cincinnati", "drillcreator")

        settings.beginGroup("MainWindow")
        settings.setValue("pos", self.geometry().topLeft())
        settings.setValue("size", (self.geometry().width(), self.geometry().height()))
        settings.setValue("last_dir", self.last_dir)
        settings.setValue("loaded_show", self.loaded_show)
        settings.endGroup()

    def draw_active_set(self):
        # clean the canvas
        # plot the points for self.active_set
        print("draw_active_set")

    def new_show(self):
        # open an existing show file and use its performers
        file_tuple = QFileDialog.getOpenFileName(self, "Use Band From Existing Show", self.last_dir, "JSON Files (*.json)")
        if file_tuple[0] != '':
            self.last_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            fp = open(file_tuple[0], 'r')
            dict = json.load(fp)
            fp.close()
            self.loaded_show = Show.fromDict(dict, True)
            self.active_set_changed.emit()

    def new_band(self):
        dialog = NewBandDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.loaded_show = Show(dialog.performers)
            self.active_set_changed.emit()

    def open(self):
        file_tuple = QFileDialog.getOpenFileName(self, "Load Show", self.last_dir, "JSON File (*.json)")
        if file_tuple[0] != '':
            self.last_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            fp = open(file_tuple[0], 'r')
            dict = json.load(fp)
            fp.close()
            self.loaded_show = Show.fromDict(dict)    
            self.active_set_changed.emit()

    def add_set_from_image(self):
        print('from image')
        self.active_set_changed.emit()

    def add_empty_set(self):
        print('empty')
        self.active_set_changed.emit()

    def add_copy_of_current_set(self):
        print('copy')
        self.active_set_changed.emit()
    
    def save(self):
        print('save')
    
    def save_as(self):
        file_tuple = QFileDialog.getSaveFileName(self, "Save Show As", self.last_dir, "JSON File (*.json)")
        if file_tuple[0] != '':
            self.last_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            fp = open(file_tuple[0], 'w')
            json.dump(self.loaded_show.toDict(), fp, indent="\t")
            fp.close()

    def previous_set(self):
        print("previous")
        self.active_set_changed.emit()
    
    def next_set(self):
        print("next")
        self.active_set_changed.emit()
    
    def toggle_navigation_mode(self):
        print("mode")
    
    def show_active_set_information(self):
        print("info")

# TODO major features
# implement existing buttons and menu bar items
# allow editing of a performer's co-ordinate in a drillset

# TODO Status Bar
# There should be a status bar at the bottom of the main window that shows the latest/current functions being performed
# by the application. For example, when solving a particularly complex drill, a message will appear stating as much. Or
# if a file was just saved, that status bar will say "File saved as 'Fake Path To File'".
