'''
@Description: TechX 2019 Recraft Resnet Transfer Learning
@Author: Tianyi Lu
@Date: 2019-07-29 17:03:08
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-30 11:53:33
'''
# -*- coding: utf-8 -*-


from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
import json

if __name__ == '__main__':
    from utils import load_valid_label
else:
    from .utils import load_valid_label

data_transforms = transforms.Compose([
        # transforms.RandomResizedCrop(224),
        # transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def predict(data_dir, img_folder):
    path = os.path.dirname(__file__)

    valid_indexs = load_valid_label(os.path.join(path,'tag.txt'))

    class ImageFolderWithPaths(datasets.ImageFolder):
        def __getitem__(self, index):
            original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
            path = self.imgs[index][0]
            tuple_with_path = (original_tuple + (path,))
            return tuple_with_path


    # Load datasets
    image_datasets = {x: ImageFolderWithPaths(os.path.join(data_dir, x), data_transforms)
                        for x in [img_folder]}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], shuffle=False)
                        for x in [img_folder]}
    dataset_sizes = {x: len(image_datasets[x]) for x in [img_folder]}
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Get labels
    model_ft = models.resnet152(pretrained=True) #using resnet152 model
    model_ft = model_ft.to(device)
    model_ft.eval()

    idx2label = []
    idx2class = {}

    with open(os.path.join(path,'imagenet_class_index.json'), 'r') as read_file:
        class_idx = json.load(read_file)
        idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
        reduced_idx2label = [idx2label[x] for x in valid_indexs]

    # Make prediction
    res = {}
    with torch.no_grad():
        for i, (inputs, labels, paths) in enumerate(dataloaders[img_folder]):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model_ft(inputs)

            # extract valid outputs
            np_outputs = outputs[0].numpy()
            reduced_np_outputs = [np_outputs[x] for x in valid_indexs]
            # print(reduced_np_outputs)
            reduced_outputs = torch.from_numpy(np.array([reduced_np_outputs]))
            # print(outputs)
            reduced_outputs = reduced_outputs.cpu().numpy().reshape(-1)
            print(reduced_outputs.shape)
            preds = reduced_outputs.argsort()[-5:][::-1]
            # _, preds = torch.max(reduced_outputs, 1)
            print(preds)

            res[paths[0].split('/')[-1]] = [reduced_idx2label[pred] for pred in preds]
            # reduced_idx2label[preds[0]]

    return res

if __name__ == '__main__':
    res = predict('data', 'train')
    print(res)



