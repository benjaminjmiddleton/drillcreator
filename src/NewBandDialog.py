from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QSpinBox

from Performer import Performer, INSTRUMENTS_LIST

class NewBandDialog(QDialog):

    def __init__(self, parent):
        self.performers = []

        super(QDialog, self).__init__(parent)
        uic.loadUi('ui/NewBandDialog.ui', self)
        self.setWindowTitle("New Band Creation")
        self.setFixedSize(self.size())

        self.buttonBox.accepted.connect(self.toPerformers)

    def toPerformers(self):
        self.performers = []
        spin_boxes = self.findChildren(QSpinBox)
        for i in range(len(spin_boxes)):
            for j in range(spin_boxes[i].value()):
                self.performers.append(Performer(INSTRUMENTS_LIST[i], j+1))
