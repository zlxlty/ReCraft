'''
@Description: Utils for res_transfer
@Author: Tianyi Lu
@Date: 2019-07-29 16:54:48
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-29 18:51:33
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

if __name__ == '__main__':
    load_valid_label('tag.txt')