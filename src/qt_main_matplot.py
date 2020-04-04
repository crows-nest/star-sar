import sys
import random

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import uic
from matplotlib import cm
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        uic.loadUi("qt_ui/mainPage_plot.ui", self)
        self.figure = plt.figure(figsize=plt.figaspect(0.5))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.Plot.setLayout(layout)
            
    def plot(self):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)

        # Normalize to [0,1]
        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape

        # Plot the surface.
        ax1 = self.figure.add_subplot(1, 1, 1, projection='3d')
        
        surf = ax1.plot_surface(X, Y, Z, rcount=rcount/2, ccount=ccount/2,
                        facecolors=colors, shade=False)
        surf.set_facecolor((0,0,0,0))

        xx, yy = np.meshgrid(np.linspace(-5,5,20), np.linspace(-5,5,20))
        data = np.random.random((20, 20))

        X = xx 
        Y = yy
        Z = (xx * 0 )
        Z = np.subtract(Z, 1)

        ax1.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=plt.cm.BrBG(data), shade=False)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    main.plot()
    sys.exit(app.exec_())

