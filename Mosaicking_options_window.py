import os
from qgis.PyQt import uic, QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Mosaicking_options_window.ui'))

class PreviewMosaicking(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, type, parent=None):
        super(PreviewMosaicking, self).__init__(parent)
        self.setupUi(self)
        self.choice=None
        if type=="Pre":
            self.label_3.setText("Maximum NDVI")
        elif type=="Post":
            self.label_3.setText("Minimum NBR")
        if self.radioButtonDate.isChecked():
            self.choice="Date"
        elif self.radioButtonIndex.isChecked():
            self.choice="Index"

        self.btnClose.clicked.connect(self.close)
