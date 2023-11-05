import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
import numpy as np

X = np.arange(1, 11)
Y = np.arange(10, 101, 10)
X, Y = np.meshgrid(X, Y)
Z = np.ndarray((10, 10))

with open("results.txt") as file:
    while line := file.readline():
        tokens = line.split()
        x_ind = int(tokens[0]) - 1
        y_ind = int(tokens[1]) // 10 - 1
        Z[x_ind, y_ind] = tokens[2]

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ls = LightSource(270, 45)
rgb = ls.shade(Z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)

plt.show()
