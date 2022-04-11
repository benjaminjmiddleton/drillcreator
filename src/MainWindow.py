from argparse import _StoreFalseAction
from os.path import expanduser
import json
import cv2

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
from Drillset import Drillset
from NewBandDialog import NewBandDialog
from image_interpreter import interpret_image

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_axis_off()
        super(MplCanvas, self).__init__(fig)
    
    def clear_points(self):
        self.axes.cla()
        self.axes.set_axis_off()
        img = plt.imread('ui/field.png')
        self.axes.imshow(img)

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

        # coord = Coordinate(-16, yardline.A_END, 4, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(-16, yardline.B_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(0, yardline.A_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # coord = Coordinate(0, yardline.B_END, 0, hashmark.FH)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'rx')

        # field_center = (self.FIELD_SIZE[0]/2, self.FIELD_SIZE[1]/2)

        # sc.axes.plot(300, 100, 'rx')
        # coord = Coordinate.from_centered_pixel_coords(300-field_center[0], 100-field_center[1], self.FIELD_SIZE)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bo')
        
        # sc.axes.plot(500, 100, 'gx')
        # coord = Coordinate.from_centered_pixel_coords(500-field_center[0], 100-field_center[1], self.FIELD_SIZE)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bo')

        # sc.axes.plot(300, 300, 'bx')
        # coord = Coordinate.from_centered_pixel_coords(300-field_center[0], 300-field_center[1], self.FIELD_SIZE)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bo')

        # sc.axes.plot(500, 300, 'yx')
        # coord = Coordinate.from_centered_pixel_coords(500-field_center[0], 300-field_center[1], self.FIELD_SIZE)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bo')

        # sc.axes.plot(400, 200, 'rx')
        # coord = Coordinate.from_centered_pixel_coords(400-field_center[0], 200-field_center[1], self.FIELD_SIZE)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bo')

        # sc.axes.plot(450, 180, 'gx')
        # coord = Coordinate.from_centered_pixel_coords(450-field_center[0], 180-field_center[1], self.FIELD_SIZE)
        # sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bo')
        
        # END PLOT TEST POINTS
        
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

        self.last_show_dir = settings.value("MainWindow/last_show_dir", defaultValue=expanduser("~"))
        self.last_image_dir = settings.value("MainWindow/last_image_dir", defaultValue=expanduser("~"))

        self.loaded_show = settings.value("MainWindow/loaded_show", defaultValue=Show([]))
        self.active_set = settings.value("MainWindow/active_set", defaultValue=None)

        self.active_set_changed.emit()
    
    def save_settings(self):
        settings = QSettings("University of Cincinnati", "drillcreator")

        settings.beginGroup("MainWindow")
        settings.setValue("pos", self.geometry().topLeft())
        settings.setValue("size", (self.geometry().width(), self.geometry().height()))
        settings.setValue("last_show_dir", self.last_show_dir)
        settings.setValue("last_image_dir", self.last_image_dir)
        settings.setValue("loaded_show", self.loaded_show)
        settings.setValue("active_set", self.active_set)
        settings.endGroup()

    def clear_points(self):
        sc = self.centralWidget().findChildren(MplCanvas)[0]
        sc.clear_points()
        sc.draw()
        
    def draw_active_set(self):
        print("draw_active_set")
        self.clear_points()
        if self.active_set != None:
            sc = self.centralWidget().findChildren(MplCanvas)[0]

            drillset = self.loaded_show.drillsets[self.active_set]
            for pid in drillset.performers_coords:
                coord = drillset.performers_coords[pid]
                sc.axes.plot(coord.get_x(self.FIELD_SIZE[0]), coord.get_y(self.FIELD_SIZE[1]), 'bx')
            sc.draw()

    def new_show(self):
        # open an existing show file and use its performers
        file_tuple = QFileDialog.getOpenFileName(self, "Use Band From Existing Show", self.last_show_dir, "JSON Files (*.json)")
        if file_tuple[0] != '':
            self.last_show_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            fp = open(file_tuple[0], 'r')
            dict = json.load(fp)
            fp.close()
            self.loaded_show = Show.fromDict(dict, True)
            self.active_set = None
            self.active_set_changed.emit()

    def new_band(self):
        dialog = NewBandDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.loaded_show = Show(dialog.performers)
            self.active_set = None
            self.active_set_changed.emit()

    def open(self):
        file_tuple = QFileDialog.getOpenFileName(self, "Load Show", self.last_show_dir, "JSON File (*.json)")
        if file_tuple[0] != '':
            self.last_show_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            fp = open(file_tuple[0], 'r')
            dict = json.load(fp)
            fp.close()
            self.loaded_show = Show.fromDict(dict)
            if len(self.loaded_show.drillsets) != 0:
                self.active_set = 0
            else:
                self.active_set = None
            self.active_set_changed.emit()

    def add_set_from_image(self):
        file_tuple = QFileDialog.getOpenFileName(self, "Add Set From Image", self.last_image_dir, "Image File (*.png *.jpeg *.jpg)")
        if file_tuple[0] != '':
            self.last_image_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            points = interpret_image(file_tuple[0], len(self.loaded_show.performers))
            print(len(self.loaded_show.performers))
            print(len(points))
            points = self.fit_to_field(points)
            shape = cv2.imread(file_tuple[0]).shape
            points = self.set_aspect_ratio(points, shape[0]/shape[1])
            coords = []
            for point in points:
                coord = Coordinate.from_centered_pixel_coords(point[0], point[1], self.FIELD_SIZE)
                coords.append(coord)
            performers_coords = {}
            for i in range(len(self.loaded_show.performers)):
                performers_coords[self.loaded_show.performers[i].performer_label()] = coords[i]
            drillset = Drillset(performers_coords, len(self.loaded_show.drillsets)+1, 32) # TODO ALLOW INPUT OF COUNTS
            if self.active_set != None:
                self.loaded_show.drillsets.insert(self.active_set+1, drillset)
                self.active_set += 1
            else:
                self.loaded_show.drillsets.append(drillset)
                self.active_set = len(self.loaded_show.drillsets)-1
            self.active_set_changed.emit()

    # given a set of points, return a tuple (min_x, max_x, min_y, max_y)
    def find_extremes(self, points):
        min_x, max_x, min_y, max_y = None, None, None, None
        for point in points:
            if min_x == None or point[0] < min_x:
                min_x = point[0]
            if max_x == None or point[0] > max_x:
                max_x = point[0]
            if min_y == None or point[1] < min_y:
                min_y = point[1]
            if max_y == None or point[1] > max_y:
                max_y = point[1]
        return min_x, max_x, min_y, max_y

    # given a set of points centered at (0,0), make sure they fit inside the field
    def fit_to_field(self, points):
        min_x, max_x, min_y, max_y = self.find_extremes(points)
        if min_x < -self.FIELD_SIZE[0]/2:
            factor = abs(min_x/(self.FIELD_SIZE[0]/2))
            points = [(point[0]/factor, point[1]) for point in points]
        if max_x > self.FIELD_SIZE[0]/2:
            factor = abs(max_x/(self.FIELD_SIZE[0]/2))
            points = [(point[0]/factor, point[1]) for point in points]
        if min_y < -self.FIELD_SIZE[1]/2:
            factor = abs(min_y/(self.FIELD_SIZE[1]/2))
            points = [(point[0], point[1]/factor) for point in points]
        if max_y > self.FIELD_SIZE[1]/2:
            factor = abs(max_y/(self.FIELD_SIZE[1]/2))
            points = [(point[0], point[1]/factor) for point in points]
        return points
    
    def set_aspect_ratio(self, points, target_ratio):
        """
        @param target_ratio: original pixel ratio of the image interpreted into the points, x/y.
        """
        min_x, max_x, min_y, max_y = self.find_extremes(points)
        width = max_x - min_x
        height = max_y - min_y
        ratio = width/height
        factor = target_ratio / ratio
        if factor < 1: # if the points are too wide
            points = [(point[0]*factor, point[1]) for point in points]
        elif factor > 1: # if the points are too tall
            points = [(point[0], point[1]/factor) for point in points]
        return points

    def add_empty_set(self):
        print('empty')
        self.active_set_changed.emit()

    def add_copy_of_current_set(self):
        print('copy')
        self.active_set_changed.emit()
    
    def save(self):
        print('save')
    
    def save_as(self):
        file_tuple = QFileDialog.getSaveFileName(self, "Save Show As", self.last_show_dir, "JSON File (*.json)")
        if file_tuple[0] != '':
            self.last_show_dir = QFileInfo(file_tuple[0]).dir().absolutePath()
            fp = open(file_tuple[0], 'w')
            json.dump(self.loaded_show.toDict(), fp, indent="\t")
            fp.close()

    def previous_set(self):
        if self.active_set != None and self.active_set > 0:
            self.active_set -= 1
            self.active_set_changed.emit()
    
    def next_set(self):
        print(self.active_set)
        if self.active_set != None and self.active_set < len(self.loaded_show.drillsets)-1:
            self.active_set += 1
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
