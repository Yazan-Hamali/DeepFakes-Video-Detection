
import os
import argparse


import torch
import pretrainedmodels
import torch.nn as nn
import torch.nn.functional as F
from network.xception import xception
import math
import torchvision


def return_pytorch04_xception(pretrained=True):
    # Raises warning "src not broadcastable to dst" but thats fine
    model = xception(pretrained=False)
    if pretrained:
        # Load model in torch 0.4+
        model.fc = model.last_linear
        del model.last_linear
        state_dict = torch.load(
            './xception-b5690688.pth')
        for name, weights in state_dict.items():
            if 'pointwise' in name:
                state_dict[name] = weights.unsqueeze(-1).unsqueeze(-1)
        model.load_state_dict(state_dict)
        model.last_linear = model.fc
        del model.fc
    return model


class TransferModel(nn.Module):
    """
    Simple transfer learning model that takes an imagenet pretrained model with
    a fc layer as base model and retrains a new fc layer for num_out_classes
    """
    def __init__(self, modelchoice, num_out_classes=2, dropout=0.0,pre=True):
        super(TransferModel, self).__init__()
        self.modelchoice = modelchoice
        self.pre=pre
        if modelchoice == 'xception':
            self.model = return_pytorch04_xception(pretrained=self.pre)
            # Replace fc
            num_ftrs = self.model.last_linear.in_features
            if not dropout:
                self.model.last_linear = nn.Linear(num_ftrs, num_out_classes)
            else:
                print('Using dropout', dropout)
                self.model.last_linear = nn.Sequential(
                    nn.Dropout(p=dropout),
                    nn.Linear(num_ftrs, num_out_classes)
                )
        else:
            raise Exception('Choose valid model')

    def fine_tune(self):

        # Stage-1: freeze all the layers
        for i, param in self.model.named_parameters():
            param.requires_grad = False
        # Make fc trainable
        for param in self.model.last_linear.parameters():
            param.requires_grad = True

    def forward(self, x):
        x = self.model(x)
        return x


def model_selection(modelname, num_out_classes,
                    dropout=None):

    if modelname == 'xception':
        return TransferModel(modelchoice='xception',num_out_classes=num_out_classes), 299, \
               True, ['image'], None
    else:
        raise NotImplementedError(modelname)


if __name__ == '__main__':
    model, image_size, *_ = model_selection('resnet18', num_out_classes=2)
    print(model)
    model = model.cuda()
    from torchsummary import summary
    input_s = (3, image_size, image_size)
    print(summary(model, input_s))
