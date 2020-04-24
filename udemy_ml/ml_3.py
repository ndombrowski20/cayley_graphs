# udemy ml scrap 3

# gradient visualization

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# print("Python: {}".format(sys.version))
# print("numpy: {}".format(np.__version__))
# print("matplotlib: {}".format(matplotlib.__version__))

nx, ny = (100, 100)
x = np.linspace(0, 10, nx)
y = np.linspace(0, 10, ny)

xv, yv = np.meshgrid(x, y)


def f(first, second):
    return first*(second**2)


z = f(xv, yv)

# print(z)

plt.figure(figsize=(14,12))
plt.pcolor(xv, yv, z)
plt.title("2D color plot of f(x, y) = xy^2")
plt.colorbar()
# plt.show()

# generate a new 2d meshgrid for the gradient

nx_1, ny_1 = (10, 10)
x_1 = np.linspace(0, 10, nx_1)
y_1 = np.linspace(0, 10, ny_1)

xg, yg = np.meshgrid(x_1, y_1)
Gy, Gx = np.gradient(f(xg, yg))

plt.quiver(xg, yg, Gx, Gy, scale = 1000, color = 'w')
# plt.show()

# checking we did it right

def ddx(x, y):
    return y**2

def ddy(x, y):
    return 2*x*y

Gx_1 = ddx(xg, yg)
Gy_1 = ddy(xg, yg)

plt.quiver(xg, yg, Gx_1, Gy_1, scale=1000, color = 'k')

# they show a bit off from one another, which is a bit confusing. not entirely sure why. i'll play with it for a while
# longer to see what's going on.

plt.show()