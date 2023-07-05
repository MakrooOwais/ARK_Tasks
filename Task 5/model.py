# import torch
# import torch.nn as nn
# import torch.nn.functional as F


# class Circle_model(nn.Module):
#     def __init__(self, input_features=8, hidden1=20, hidden2=10, out_features=4):
#         super().__init__()
#         self.f_connected2 = nn.Linear(input_features, hidden1)
#         self.f_connected3 = nn.Linear(hidden1, hidden2)
#         self.out = nn.Linear(hidden2, out_features)

#     def forward(self, x):
#         x = F.relu(self.f_connected2(x))
#         x = F.relu(self.f_connected3(x))
#         x = self.out(x)
#         return x

#     def save(self, model, model_path):
#         torch.save(model.state_dict(), model_path)

#     def load(self, model_path):
#         self.load_state_dict(torch.load(model_path))

#         self.eval()

import torch
import torch.nn.functional as F


class Circle_model(torch.nn.Module):

    def __init__(self):
        super(Circle_model, self).__init__()
        # 1 input image channel (black & white), 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = torch.nn.Conv2d(1, 6, 9)
        self.conv2 = torch.nn.Conv2d(6, 16, 6)
        # an affine operation: y = Wx + b
        self.fc1 = torch.nn.Linear(16 * 450 * 190, 1200)  # 6*6 from image dimension
        self.fc2 = torch.nn.Linear(1200, 840)
        self.fc3 = torch.nn.Linear(840, 100)
        self.fc4 = torch.nn.Linear(100, 25)
        self.fc5 = torch.nn.Linear(25, 4)


    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features