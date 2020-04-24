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
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        X = np.vstack((X, row[:-1]))
        Y = np.append(Y, float(row[-1]))

X = np.delete(X, 0, 0)

print(X.shape)
print(Y.shape)

X = tch.tensor(X).float()
Y = tch.tensor(Y).float()

# defining our neural net, inputs:25, output: 1,

MyLinearNet = nn.Linear(25, 1)

# taking the transposes
if X.shape[1]!=25:
   X=X.t()
print("size of X=",X.shape)

# Now we set up the SGD

optimizer = optim.SGD(MyLinearNet.parameters(), lr=0.0001)

# This defines the loss function as MSE

MyLossFun = nn.MSELoss()

# and here we go


def zero_grad_step(optim, X, Y, MLN):
    L = tch.tensor(100)
    print(L)
    print(L.item())
    i = 0
    while L > 0.01 and i < 100:
        i += 1
        optim.zero_grad()
        Yhat = MLN(X)
        print(Yhat.shape)
        print(Yhat)
        print(Y.shape)
        L = MyLossFun(Yhat, Y)
        print(L.item())
        L.backward()
        optim.step()
        print(i)


zero_grad_step(optimizer, X, Y, MyLinearNet)


def reg_grad_step(optimizer, X, Y, MyLinearNet):
  L=tch.tensor(100)
  i=0
  while L>0.01 and i<100:
    i+=1
    Yhat=MyLinearNet(X)
    L = MyLossFun(Yhat, Y)
    print(L.item())
    L.backward()
    optimizer.step()

# reg_grad_step(optimizer, X, Y, MyLinearNet)
