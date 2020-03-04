#! /usr/bin/python3


from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np



 #ake data.
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

#print(X, Y, Z)
 
ax1.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=plt.cm.BrBG(data), shade=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

