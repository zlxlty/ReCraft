'''
@Description: Utils for res_transfer
@Author: Tianyi Lu
@Date: 2019-07-29 16:54:48
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-29 17:52:27
'''
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import copy
import json
import os
import matplotlib.pyplot as plt

def load_valid_label(file_name):
    labels = []
    with open(file_name, 'r') as f:
        labels = f.readlines()
        labels = [int(label.strip('\n')) for label in labels]
        # print(labels)
    return labels

def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

if __name__ == '__main__':
    load_valid_label('tag.txt')