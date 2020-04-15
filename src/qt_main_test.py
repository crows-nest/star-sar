import sys
import random

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import uic
from matplotlib import cm
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.image as mpimg
from matplotlib._png import read_png
from mpl_toolkits.mplot3d import Axes3D


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        uic.loadUi("./qt_ui/mainPage.ui", self)

        # Plot Layout
        self.figure = plt.figure(figsize=(16, 9), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.Plot.setLayout(layout)

        self.toggles = {'Satellite Data': True, 'Human Motion Model': True, 'RF Model': True, 'Fused Data Model': True}
        self.views = {'2d': self.plot2d, '3d': self.plot3d}
        
        # Map Vars
        self.res = 30
        self.refresh_rate = 30
        self.alpha = 3

        # Setup Calls
        self.view_setup()
        self.layer_setup()
        self.slider_setup()

        # Initail View
        self.views['2d']()

    def view_setup(self): 
        self.view_sel.currentIndexChanged.connect(self.selectionchange)
        
    def selectionchange(self): 
        a = self.views[self.view_sel.currentText()]()
    
    def slider_setup(self):
        self.resolution.valueChanged.connect(self.sliderMoved)
        self.resolution.setMinimum(10)
        self.resolution.setMaximum(100)
        self.resolution.setValue(10)

        self.refresh.valueChanged.connect(self.sliderMoved)
        self.refresh.setMinimum(10)
        self.refresh.setMaximum(100)
        self.refresh.setValue(100)

        self.transparency.valueChanged.connect(self.sliderMoved)
        self.transparency.setMinimum(0)
        self.transparency.setMaximum(10)
        self.transparency.setValue(3)

    def layer_setup(self): 
        self.sat.stateChanged.connect(lambda:self.button_state(self.sat))
        self.sat.toggle()

        self.human.stateChanged.connect(lambda:self.button_state(self.human))
        self.human.toggle()

        self.rf.stateChanged.connect(lambda:self.button_state(self.rf))
        self.rf.toggle()

        self.fuse.stateChanged.connect(lambda:self.button_state(self.fuse))
        self.fuse.toggle()

    def button_state(self,b):
        if b.isChecked():
            self.toggles[b.text()] = True
            self.views[self.view_sel.currentText()]()
        else: 
            self.toggles[b.text()] = False
            self.views[self.view_sel.currentText()]()     

    def sliderMoved(self):
        self.res = self.resolution.value()
        self.alpha = self.transparency.value()

        self.views[self.view_sel.currentText()]()

    def plot2d(self):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)

        # Normalize to [0,1]
        norm = plt.Normalize(Z.min(), Z.max())
        cmap = plt.get_cmap('jet')

        if self.toggles['Fused Data Model']: surf = ax.contourf(X, Y, Z, alpha=float(self.alpha)/10, antialiased=True, cmap=cmap)

        arr = mpimg.imread("/Users/jakemcgrath/Desktop/star-sar/star-sar-ui_integration/src/test.png")
        extent = ax.get_xlim()+ ax.get_ylim()

        if self.toggles['Satellite Data']:ax.imshow(arr, extent=extent)



        self.canvas.draw()

    def plot3d(self):
        self.figure.clear()
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

        arr = mpimg.imread("/Users/jakemcgrath/Desktop/star-sar/star-sar-ui_integration/src/test.png")
        height, width = arr.shape[:2]
        # 10 is equal length of x and y axises of your surface
        stepX, stepY = self.res/width, self.res/height

        X1 = np.arange(-5, 5, stepX)
        Y1 = np.arange(-5, 5, stepY)
        X1, Y1 = np.meshgrid(X1, Y1)
        ax1.plot_surface(X1, Y1, np.atleast_2d(-2.0), rstride=10, cstride=10, facecolors=arr)



        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()

    
    sys.exit(app.exec_())

