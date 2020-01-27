import numpy as np
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

angles = np.arange(40)

# function for the norm


def v_norm(x):
    sum = 0
    for i in x:
        sum += i**2
    return sum**.5


# function for angle calculation


def angle_calc(x, y):
    numerator = 0
    for i in range(len(x)):
        numerator += x[i]*y[i]
    denominator = v_norm(x)*v_norm(y)
    ans = np.arccos(numerator/denominator)
    return np.degrees(ans)


# here n serves as the number of DIMENSIONS, and m is the number of PAIRS that will be generated


def generate_vectors(n, m):
    print(n)
    print(m)


y = [1, 10, 15]
z = [0, 1, 1]

print(angle_calc(y, z))


L = np.random.normal(1.0, 0.005, 100)

plt.figure()
plt.hist(angles, 100)
plt.xlim(0, 180)
plt.xlabel("angle (degrees)")
plt.ylabel("count")
# plt.show()