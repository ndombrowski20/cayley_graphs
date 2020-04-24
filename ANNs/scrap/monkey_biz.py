import torch.nn as nn
import torch as tch
import torch.optim as optim
import numpy as np
import csv
import pandas as pd
import time as time


# this is our x and y data
i = 0
X = np.arange(0, 25)
Y = np.array([])

start = time.time()

with open('data_small.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        X = np.vstack((X, row[:-1]))
        Y = np.append(Y, [row[-1]])

X = np.delete(X, 0, 0)

X = tch.tensor(X).float()
Y = tch.tensor(Y).float()

# defining our neural net, inputs:25, output: 1,

MyLinearNet = nn.Linear(25, 1)

# taking the transposes
if X.shape[1]!=25:
   X=X.t()
print("size of X=",X.shape)

# Now we set up the SGD

optimizer = optim.SGD(MyLinearNet.parameters(), lr=.00000000000005005)

# This defines the loss function as MSE

MyLossFun = nn.MSELoss()

# and here we go

def zero_grad_step(optim, X, Y, MLN):
    L = tch.tensor(100)
    i = 0
    L_trend = []
    while L > 0.1 and i < 1000:
        i += 1
        optim.zero_grad()
        Yhat = MLN(X)
        L = MyLossFun(Yhat, Y)
        L_trend.append(L.item())
        L.backward()
        optim.step()
    print(L_trend)


zero_grad_step(optimizer, X, Y, MyLinearNet)

print(time.time() - start)
