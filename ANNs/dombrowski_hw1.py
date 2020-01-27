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


# generate a normally distributed random vector.


def generate_vector(n):
    vector = []
    for i in range(n):
        vector.append(np.random.normal(100.0, 10))
    return vector



y = [1, 10, 15]
z = [0, 1, 1]

print(angle_calc(generate_vector(2), generate_vector(2)))


L = np.random.normal(1.0, 0.005, 100)

plt.figure()
plt.hist(angles, 100)
plt.xlim(0, 180)
plt.xlabel("angle (degrees)")
plt.ylabel("count")
# plt.show()