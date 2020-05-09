import os

import cv2
import numpy as np
import torch
import torch.autograd as autograd
import torch.nn as nn

from model.network import SetNet


class GetFeature:
    def __init__(self, encoder_path):
        self.encoder = SetNet(256).float()
        self.encoder = nn.DataParallel(self.encoder)
        self.encoder.cuda()
        self.encoder.load_state_dict(torch.load(encoder_path))

    def ts2var(self, x):
        return autograd.Variable(x).cuda()

    def np2var(self, x):
        return self.ts2var(torch.from_numpy(x))

    def transform(self, frames):
        self.encoder.eval()
        feature_list = list()
        for batch_frame in frames:
            if batch_frame is not None:
                batch_frame = self.np2var(batch_frame).int()
            feature, _ = self.encoder(_, batch_frame)
            feature_list.append(feature)
        return np.concatenate(feature_list, 0)

    def cut_img(self, img):
        # A silhouette contains too little white pixels
        # might be not valid for identification.
        if img.sum() <= 10000:
            print("Image doesn't have enough data")
            return None
        # Get the top and bottom point
        t_h = 64
        t_w = 64
        y = img.sum(axis=1)
        y_top = (y != 0).argmax(axis=0)
        y_btm = (y != 0).cumsum(axis=0).argmax(axis=0)
        img = img[y_top:y_btm + 1, :]
        # As the height of a person is larger than the width,
        # use the height to calculate resize ratio.
        _r = img.shape[1] / img.shape[0]
        _t_w = int(t_h * _r)
        img = cv2.resize(img, (_t_w, t_h), interpolation=cv2.INTER_CUBIC)
        # Get the median of x axis and regard it as the x center of the person.
        sum_point = img.sum()
        sum_column = img.sum(axis=0).cumsum()
        x_center = -1
        for i in range(sum_column.size):
            if sum_column[i] > sum_point / 2:
                x_center = i
                break
        if x_center < 0:
            print("No center")
            return None
        h_t_w = int(t_w / 2)
        left = x_center - h_t_w
        right = x_center + h_t_w
        if left <= 0 or right >= img.shape[1]:
            left += h_t_w
            right += h_t_w
            _ = np.zeros((img.shape[0], h_t_w))
            img = np.concatenate([_, img, _], axis=1)
        img = img[:, left:right]
        return img.astype('uint8')

    def extract_feature(self, silhouettes_path):
        frames = list()
        for img in os.listdir(silhouettes_path):
            frames.append(self.cut_img(cv2.imread(
                os.path.join(silhouettes_path, img))))
        return self.transform(frames)

