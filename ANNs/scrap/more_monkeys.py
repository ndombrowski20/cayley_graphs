import torch  # We no longer import as tch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from time import time as tm
import csv

i = 0
T = np.arange(0, 26)
X = np.arange(0, 25)
Y = np.array([])

with open('data_small.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        T = np.vstack((T, row))
        X = np.vstack((X, row[:-1]))
        Y = np.append(Y, [row[-1]])

T = np.delete(T, 0, 0)
X = np.delete(X, 0, 0)

X = torch.tensor(X).float()
Y = torch.tensor(Y).float()

# T = torch.tensor(T).float()

# train_dataset = torchvision.datasets.MNIST(root='./',
#                                            train=True,
#                                            transform=transforms.ToTensor(),
#                                            download=True)
# test_dataset = torchvision.datasets.MNIST(root='./',
#                                           train=False,
#                                           transform=transforms.ToTensor(),
#                                           download=True)
# # Print the size of the two data sets
# m = len(train_dataset)
# mtest = len(test_dataset)
# print("Data points in training set=", m, "; in test set=", mtest)
#
# # train_dataset.data contains all the MNIST images (X)
# # train_dataset.targets contains all the labels (Y)
# print("Size of training inputs (X)=", train_dataset.data.size())
# print("Size of training labels (Y)=", train_dataset.targets.size())
# ########


########
# Set some hyperparameters
num_epochs = 5  # Number of times to go through training data
batch_size = 300  # Batch size to use with training data
epsilon = .2  # Learning rate
test_batch_size = 200  # Batch size to use for test data

# Data loader. These provide useful functions for iterating through
# batches of data.
# Shuffle=True means that the data will be randomly shuffled on every epoch
train_loader = torch.utils.data.DataLoader(dataset=T,
                                           batch_size=batch_size,
                                           shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=Y,
                                          batch_size=test_batch_size,
                                          shuffle=True)

TrainingIterator = iter(train_loader)
A = next(TrainingIterator)
print(A)
print("Size of one X batch=", X.size())
print("Size of one Y batch=", Y.size())


########


########
# Make a neural net. First define the functions
# that make up all the layers. Then compose the
# neural network as the "forward" pass
# The forward function is what gets called when you
# pass an input, x, to the network
class MyMNISTclassifier(nn.Module):
    def __init__(self):
        super(MyMNISTclassifier, self).__init__()
        self.Lin1 = nn.Linear(28 * 28, 1000)
        self.Lin2 = nn.Linear(1000, 300)
        self.Lin3 = nn.Linear(300, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.Lin1(x)
        out = self.relu(out)
        out = self.Lin2(out)
        out = self.relu(out)
        out = self.Lin3(out)
        return out


# Use 'cpu' for cpu and 'cuda' for gpu
# If you choose 'cuda' then make sure you change Runtime type to GPU
device = 'cpu'
model = MyMNISTclassifier().to(device)

# Use cross-entropy loss.
# This means we will use the softmax loss function discussed in Notes4*
criterion = nn.CrossEntropyLoss()

# Use SGD to optimize
optimizer = torch.optim.SGD(model.parameters(), lr=epsilon)

# Compute and print number of trainable parameters
NumParams = sum(p.numel() for p in model.parameters() if p.requires_grad)
print('Number of parameters in model =', NumParams)
########


########
# There are 60000 images in the training data. If we're using
# a batch size of 200, then there are 300 gradient descent steps
# per epoch. We then repeat this num_epochs times for a total
# of num_epochs*steps_per_epoch steps.
steps_per_epoch = len(train_loader)
total_num_steps = num_epochs * steps_per_epoch
LossesToPlot = np.zeros(total_num_steps)  # Initialize vector of losses
print("steps per epoch=", steps_per_epoch, "\nnum epochs=", num_epochs, "\ntotal number of steps=", total_num_steps)
########


# ########
# j = 0
# t1 = tm()
# for k in range(num_epochs):
#     TrainingIterator = iter(train_loader)
#     for i in range(steps_per_epoch):
#
#         # Get one batch of training data, reshape it
#         # and send it to the current device
#         X, Y = next(TrainingIterator)
#         X = X.reshape(-1, 28 * 28).to(device)
#         Y = Y.to(device)
#
#         # Forward pass: compute yhat and loss for this batch
#         Yhat = model(X)
#         Loss = criterion(Yhat, Y)
#
#         # Backward pass and optimize
#         optimizer.zero_grad()  # Zero-out gradients from last iteration
#         Loss.backward()  # Compute gradients
#         optimizer.step()  # Update parameters
#
#         # Store loss and increment counter
#         LossesToPlot[j] = Loss.item()
#         j += 1
#
#         # Print loss every 100 steps
#         if (i + 1) % 100 == 0:
#             print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(k + 1, num_epochs, i + 1, steps_per_epoch,
#                                                                      Loss.item()))
# t2 = tm()
# print("Training time=", t2 - t1, "sec=", (t2 - t1) / num_epochs, "sec/epoch=", (t2 - t1) / total_num_steps, "sec/step")
#
# # Plot losses
# plt.plot(LossesToPlot)
# plt.xlabel("Iteration")
# plt.ylabel("Loss")
#
# # Compute and print misclassification rates on train and test set
# with torch.no_grad():
#     X = train_dataset.data.reshape(-1, 28 * 28).to(device)
#     Y = train_dataset.targets.to(device)
#     Yhat = model(X.float())
#     PredictedClass = torch.argmax(Yhat.data, 1)
#     TrainingMisclassRate = 1 - (PredictedClass == Y).sum().item() / Y.size(0)
#     print('Percent of training images misclassified: {} %'.format(100 * TrainingMisclassRate))
#
#     Xtest = test_dataset.data.reshape(-1, 28 * 28).to(device)
#     Ytest = test_dataset.targets.to(device)
#     YhatTest = model(Xtest.float())
#     PredictedClassTest = torch.argmax(YhatTest.data, 1)
#     TestMisclassRate = 1 - (PredictedClassTest == Ytest).sum().item() / Ytest.size(0)
#     print('Percent of testing images misclassified:  {} %'.format(100 * TestMisclassRate))