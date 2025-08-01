import torch
import torchvision
import torchvision.transforms as transforms
import requests
from torchscope.scope import *


# url = "http://127.0.0.1:8000/user/register"
# data = {
#         "model": "23439852038309",
#         "project": "test_project", 
#         "schema": {
#             "iteration": "INTEGER",
#             "loss": "FLOAT",
#         },
# }
# response = requests.post(url, json=data)
# run_id = response.json().get("run_id")
# print(f"Run ID: {run_id}")
# exit()

# url = "http://127.0.0.1:8000/user/data"


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 80)
        self.fc3 = nn.Linear(80, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net().to(DEVICE)

scope = Scope("CIFAR10_Training", net)
loss_scope = scope.get_data_handle("loss", DataType.FLOAT)
scope.register()


import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs.to(DEVICE))
        loss = criterion(outputs, labels.to(DEVICE))
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
            loss_scope.update(running_loss / 2000)
            # loss_scope.update(0.0)
            scope.update((i+1) + (epoch+1) * len(trainloader))
            running_loss = 0.0
            # data = [
            #     {
            #         "iteration": i + 1,
            #         "loss": loss.item(),
            #     }
            # ]
            # response = requests.post(url, json={"run_id": run_id, "data": data})
        # if response.status_code == 200:
        #     print("Data registered successfully.")

print('Finished Training')
