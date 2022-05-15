from PyQt5 import QtGui,QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QThread

class MplCanvas(FigureCanvas,QThread):
    def __init__(self):
        self.fig = Figure(figsize=(2,2),facecolor='white')
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fig.set_size_inches(2,2)

class plotwidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()    
        self.canvas.axes = self.canvas.figure.add_subplot(111,facecolor='white')
        self.canvas.axes.set_xlabel('Spectral Displacement(m)', fontsize=8, color='black')
        self.canvas.axes.set_ylabel('Spectral Acceleration/g', fontsize=8, color='black')
        self.canvas.axes.set_title('Sa vs Sd', fontsize=10, color='black',weight='bold')
        self.canvas.axes.set_xlim(left=0)
        self.canvas.axes.set_ylim(bottom=0)
        self.canvas.axes.tick_params(axis='both', which='major', labelsize=8, labelcolor='black')
        self.canvas.axes.grid(True,linestyle='--', color='black',alpha=0.3)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.canvas.axes.get_images()



