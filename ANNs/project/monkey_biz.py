import torch.nn as nn
import torch as tch
import torch.optim as optim
import numpy as np
import csv
import pandas as pd


# this is our x and y data
i = 0
X = np.arange(0, 25)
Y = np.array([])

with open('data_full.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    for row in reader:
        print(row)

print(X.shape)
print(Y.shape)
