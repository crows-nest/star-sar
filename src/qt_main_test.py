#! /usr/bin/python3

#TODO no reference to crowsnest.qrc 
#TODO add 3D_dist for exampe display


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


def test_plot():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import numpy as np

     #make data.
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)

    # Normalize to [0,1]
    norm = plt.Normalize(Z.min(), Z.max())
    colors = cm.viridis(norm(Z))
    rcount, ccount, _ = colors.shape

    fig = plt.figure(figsize=plt.figaspect(0.5))
    # Plot the surface.
    ax1 = fig.add_subplot(1, 1, 1, projection='3d')
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

    return plt

if __name__ == "__main__":

    test = test_plot()
    test.show()
    
    
    Form, Window = uic.loadUiType("qt_ui/searchHomePage.ui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    app.exec_()


