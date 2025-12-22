import os
import requests
from qgis.PyQt import uic, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout,QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'owa_parameters_window.ui'))

class OwaParametersWindow(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, n_features, parent=None):
        
        super(OwaParametersWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.canvas = PlotCanvas(n_features, self.plotWidget)
        layout = QVBoxLayout(self.plotWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.result = None
        self.btnClose.clicked.connect(self.accept)
        
    def accept(self):
        self.result = [self.canvas.p1[0], self.canvas.p2[0]]
        super().accept()
            
        

class PlotCanvas(FigureCanvas):
    def __init__(self, n_features, parent=None):
        fig_width_inches = 5
        fig_height_inches = 4
        self.fig, self.ax = plt.subplots(figsize=(fig_width_inches, fig_height_inches))
        super().__init__(self.fig)
        self.setParent(parent)

        # Points: P0 (fixed), P1 (mobile), P2 (mobile), P3 (fixed)
        self.p0 = (0, 0)
        self.p1 = [2, 0]     # mobile on X
        self.p2 = [6, 1]     # mobile on X
        self.p3 = (n_features+1, 1)

        self.n_features = n_features
        self.dragging = None
        self.plot()

        # Mouse events
        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('motion_notify_event', self.on_drag)
        self.mpl_connect('button_release_event', self.on_release)

    def plot(self, highlight_index=None):
        self.ax.clear()
        self.fig.subplots_adjust(
            left=0.15,    # Left space (for Y labels)
            right=0.95,   # Right space
            bottom=0.23,  # Bottom space (for X labels)
            top=0.85,     # Top space (for title)
            wspace=0.2, 
            hspace=0.2
        )
        x = [self.p0[0], self.p1[0], self.p2[0], self.p3[0]]
        y = [self.p0[1], self.p1[1], self.p2[1], self.p3[1]]
        
        for i, pt in enumerate([self.p1, self.p2]):
            size = 16 if i == highlight_index else 8
            color = 'orange' if i == highlight_index else 'blue'
            self.ax.plot(pt[0], pt[1], 'o', color=color, markersize=size)
        
        self.ax.plot(x, y, linestyle='-', markersize=8)
        self.ax.set_xlim(0, self.n_features+1)
        self.ax.set_ylim(-0.5, 1.5)
        self.ax.set_xlabel("N. of features with non-zero evidence, necessary (a) and sufficient (b) ")
        self.ax.set_xticks(range(self.n_features + 1))
        self.ax.set_ylabel("Weight")
        self.ax.set_yticks([0, 0.5, 1])
        self.ax.set_title("Parameters: a = " + str(self.p1[0]) + ", b = " + str(self.p2[0]))
        self.draw()
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        for i, pt in enumerate([self.p1, self.p2]):
            if abs(pt[0] - event.xdata) < 0.3 and abs(pt[1] - event.ydata) < 0.5:
                self.dragging = i
                break

    def on_drag(self, event):
        if self.dragging is None or event.inaxes != self.ax:
            return
        if self.dragging == 0:
            new_x = int(max(0, min(self.n_features + 0.001, event.xdata, self.p2[0])))  #horizontal limits integers
            self.p1[0] = new_x
        elif self.dragging == 1:
            new_x = int(max(max(1, self.p1[0]), min(self.n_features + 0.001, event.xdata)))  #horizontal limits integers
            self.p2[0] = new_x
        self.plot(highlight_index=self.dragging)

    def on_release(self, event):
        self.dragging = None



