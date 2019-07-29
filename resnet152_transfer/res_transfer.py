'''
@Description: TechX 2019 Recraft Resnet Transfer Learning
@Author: Tianyi Lu
@Date: 2019-07-29 17:03:08
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-29 17:52:58
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
import utils

data_transforms = {
    'train': transforms.Compose([
        # transforms.RandomResizedCrop(224),
        # transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

def visualize_model(model, classes, valid_indexs, num_images=6):
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, (inputs, labels) in enumerate(dataloaders['train']):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)

            # extract valid outputs
            np_outputs = outputs[0].numpy()
            reduced_np_outputs = [np_outputs[x] for x in valid_indexs]
            # print(reduced_np_outputs)
            reduced_outputs = torch.from_numpy(np.array([reduced_np_outputs]))
            # print(outputs)
            _, preds = torch.max(reduced_outputs, 1)

            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images//2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(classes[preds[j]]))
                utils.imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)

if __name__ == '__main__':

    plt.ion()   # interactive mode
    valid_indexs = utils.load_valid_label('tag.txt')


    # Load datasets
    data_dir = 'data'
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                            data_transforms[x])
                    for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x],
                                                shuffle=True)
                for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Get labels
    model_ft = models.resnet152(pretrained=True) #using resnet152 model
    model_ft = model_ft.to(device)
    model_ft.eval()

    idx2label = []
    idx2class = {}

    with open("imagenet_class_index.json", 'r') as read_file:
        class_idx = json.load(read_file)
        idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
        reduced_idx2label = [idx2label[x] for x in valid_indexs]
        # print(reduced_idx2label)
        # with open('tag.txt', 'a') as f:
        #     for i in range(len(idx2label)):
        #         f.write(idx2label[i]+'\n')
        visualize_model(model_ft, reduced_idx2label, valid_indexs,8)

    plt.ioff()
    plt.show()




