import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import torch.utils.data as tud
import numpy as np
mnist_train_data = datasets.MNIST("./data", train=True,download=True,transform=transforms.Compose([transforms.ToTensor()]))
mnist_test_data = datasets.MNIST("./data", train=False,download=True,transform=transforms.Compose([transforms.ToTensor()]))
train_dataloader = tud.DataLoader(mnist_train_data,batch_size=64,shuffle=True)
test_dataloader = tud.DataLoader(mnist_test_data,batch_size=64,shuffle=False)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1,20,5,1)
        self.conv2 = nn.Conv2d(20,50,5,1)
        self.fc1 = nn.Linear(4*4*50,500)
        self.fc2 = nn.Linear(500,10)
    def forward(self,x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x,2,2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x,2,2)
        x = x.view(-1,4*4*50) # ?
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x,dim=1)

model = Net()

loss_fn = nn.CrossEntropyLoss()
lr = 0.01
momentum = 0.5
optimizer = optim.SGD(model.parameters(),lr=lr,momentum=momentum)

def train(model,train_dataloader,loss_fn,optimizer,epoch):
    model.train()
    for idx, (data, label) in enumerate(train_dataloader):
        output = model(data)
        loss = loss_fn(output, label)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if idx % 100 == 0:
            print("Train Epoch:{}, iteration:{}, loss:{}".format(epoch, idx, loss.item()))

def test(model, test_dataloader, loss_fn):
    model.eval()
    total_loss = 0.
    correct = 0.
    with torch.no_grad():
        for idx, (data, label) in enumerate(test_dataloader):
            output = model(data)
            loss = loss_fn(output, label)
            pred = output.argmax(dim=1)
            total_loss += loss
            correct += pred.eq(label).sum()
            print("correct:", correct)
    total_loss /= len(test_dataloader.dataset)
    acc = 100.*correct/len(test_dataloader.dataset)
    print("Test Loss:{}, Accuracy:{}%".format(total_loss,acc))

num_epochs = 2
for epoch in range(num_epochs):
    train(model,train_dataloader,loss_fn,optimizer,epoch)
    test(model,test_dataloader,loss_fn)

torch.save(model.state_dict(),"mnist_cnn.pth")