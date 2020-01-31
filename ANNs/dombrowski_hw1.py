import numpy as np
import matplotlib.pyplot as plt

# ===== part 1 =====
# function for the norm


def v_norm(x):
    sum = 0
    for i in x:
        sum += i**2
    return sum**.5


# function for angle calculation


def angle_calc(x, y):
    numerator = x@y
    denominator = v_norm(x)*v_norm(y)
    ans = np.arccos(numerator/denominator)
    return np.degrees(ans)


# generate a normally distributed random vector. i hard coded the particular mean and standard deviation.
# considering we are measuring angle, and the vectors are distributed in the same , the length shouldn't matter


def generate_vector(n):
    vector = []
    for i in range(n):
        vector.append(np.random.normal(1.0, .05))
    return vector


# generates m pairs of vectors and calculates the angle between them, storing all resulting angles in a list.
# n indicates the dimension of the vector, m indicates, ultimately, the number of angles calculated

def generate_angles(n_list, m):
    angle_list = []
    for n in n_list:
      angle_list_n = []
      angle_list_n.clear()
      for i in range(m):
          new_angle = angle_calc(np.random.normal(0.0, .05, n), np.random.normal(0.0, .05, n))
          angle_list_n.append(new_angle)
      angle_list.append(angle_list_n)
    return angle_list

assignment = generate_angles([2, 10, 100], 5*10**4)

# i don't want my machine to build the plot every time so i just wrote it into a function i could call
# also, i made the histograms overlap cause it kinda looks cool, but there's a version with different histograms


def plot_angles(angle_list):
    plt.figure()
    for i in range(len(angle_list)):
      plt.hist(angle_list[i], 100)
    plt.xlim(0, 180)
    plt.xlabel("angle (degrees)")
    plt.ylabel("count")
    plt.title("Distribution of Angles between pairs of Normally Distributed Random Vectors")
    plt.show()


def plot_angles_boring(angle_list):
    for i in range(len(angle_list)):
      plt.figure()
      plt.hist(angle_list[i], 100)
      plt.xlim(0, 180)
      plt.xlabel("angle (degrees)")
    plt.show()


plot_angles(assignment)
# plot_angles_boring(assignment)

# ===== part 2 =====


from time import time as tm

# now, we make myProduct


def myProduct(u, v):
    # check yourself before you wreck yourself
    if not isinstance(u, np.ndarray):
        raise Exception("u needs to be a numpy array (u is the first one)")
    if not isinstance(v, np.ndarray):
        raise Exception("v needs to be a numpy array (v is the second one)")
    if np.shape(u[1]) != np.shape(v[0]):
        raise Exception("at least give me some matrices i can actually take the product of")

    C = []
    for i in range(len(u)):
        Ci = []
        Ci.clear()
        for j in range(len(u[i])):
            Cij = 0
            for k in range(len(u[i])):
                Cij += u[i][k] * v[k][j]
            Ci.append(Cij)
        C.append(Ci)
    return np.asarray(C)


# now we make a function which tests how well i made myProduct


def test_myProduct(n):
    a = np.random.rand(n, n)
    b = np.random.rand(n, n)
    tm1 = tm()
    c = myProduct(a, b)
    tm2 = tm()
    mine = tm2-tm1
    print("my time = " + str(mine) + " seconds")

    tm3 = tm()
    c_np = a@b
    tm4 = tm()
    theirs = tm4-tm3
    print("their time = " + str(tm4-tm3) + " seconds")
    print("difference (mine - theirs) = " + str(mine-theirs) + " seconds")
    print(c)
    print(c_np)


# test_myProduct(100)


