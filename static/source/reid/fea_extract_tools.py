import os, sys, json
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
from torchvision import datasets, transforms
import torch.backends.cudnn as cudnn
import scipy.io
import matplotlib
import yaml
import math
import matplotlib.pyplot as plt
from model import ft_net, PCB, PCB_test

matplotlib.use('Agg')


#   Part 1  Network Dealing
###################################################################
def load_network(network):
    save_path = './model/net_last.pth'
    network.load_state_dict(torch.load(save_path))
    return network


def fliplr(img):  # 水平左右翻转
    inv_idx = torch.arange(img.size(3) - 1, -1, -1).long()  # N x C x H x W
    img_flip = img.index_select(3, inv_idx)
    return img_flip


def extract_feature(model, dataloaders):
    features = torch.FloatTensor()
    count = 0

    # Load Data
    for data in dataloaders:
        img, label = data
        n, c, h, w = img.size()
        count += n
        # print(count)

        # ff = torch.FloatTensor(n, 1024).zero_()   # ResNet and DenseNet
        ff = torch.FloatTensor(n, 2048, 6).zero_().cuda()   # PCB, if cpu comment cuda

        for i in range(2):
            if i == 1:
                img = fliplr(img)
            input_img = Variable(img.cuda())
            outputs = model(input_img)
            # f = outputs.data.cpu()
            ff = ff + outputs

        # get norm feature

        # PCB
        # feature size (n,2048,6)
        # 1. To treat every part equally, I calculate the norm for every 2048-dim part feature.
        # 2. To keep the cosine score==1, sqrt(6) is added to norm the whole feature (2048*6).
        f_norm = torch.norm(ff, p=2, dim=1, keepdim=True) * np.sqrt(6)
        ff = ff.div(f_norm.expand_as(ff))
        ff = ff.view(ff.size(0), -1)

        # ResNet
        # f_norm = torch.norm(ff, p=2, dim=1, keepdim=True)
        # ff = ff.div(f_norm.expand_as(ff))

        features = torch.cat((features, ff.data.cpu()), 0)
    return features


###############################################################################


#   Part 2 Data Dealing
###############################################################################
def get_id(img_path):
    # 照片文件名字格式： c1_p1_t1_f001.jpg
    cam_ids = []    # camera
    labels = []     # camera + person
    indexes = []    # track + frame
    for path, path_index in img_path:   # dataset每一个都返回一个二元组，图片地址，图片子文件夹序号
        filename = os.path.basename(path)   # 图片名
        camera0 = filename.split("_")[0]
        camera = camera0.split("c")[1]
        label0 = filename.split("p")[1]
        label = camera + "951" + label0.split('_')[0]   # 用951来作为中间的区分
        pic_idx0 = filename.split("t")[1]
        pic_frame = pic_idx0.split("f")[1]
        pic_frame = pic_frame.split(".")[0].zfill(5)    # 5位
        pic_idx1 = pic_idx0.split("_")[0].zfill(3)               # 3位
        pic_idx = pic_idx1+pic_frame    # 3位tid+ 5位frame

        labels.append(int(label))
        cam_ids.append(int(camera))
        indexes.append(int(pic_idx))

    return cam_ids, labels, indexes


def store_all_in_mat(test_dir, save_mat_dir):
    #############################
    # GPU设置
    gpu_ids = [0]
    if len(gpu_ids) > 0:
         torch.cuda.set_device(gpu_ids[0])
         cudnn.benchmark = True
    use_gpu = torch.cuda.is_available()

    #############################
    # 1. 文件读取部分
    # baseline通用的data_transforms转换设置
    data_transforms = transforms.Compose([
        transforms.Resize((384, 192), interpolation=3),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # datasets 和 dataloader
    data_dir = test_dir
    image_datasets = datasets.ImageFolder(data_dir, data_transforms)
    dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=8,
                                              shuffle=False, num_workers=0)
    # class_names = image_datasets.classes

    data_path = image_datasets.imgs     # 这里的返回值是一个tuple组成的list (文件路径，第几个子文件夹)

    ############
    # 第一个调用，是按照原顺序的三个list
    camera_id, data_label, pic_index = get_id(data_path)

    #############################
    # 2. 提取部分
    # model载入
    # model_structure = ft_net(751)
    model_structure = PCB(751)
    model = load_network(model_structure)
    model = PCB_test(model)
    model.model.fc = nn.Sequential()
    model.classifier = nn.Sequential()
    model = model.eval()
    model = model.cuda()
    # 提取特征
    feature = extract_feature(model, dataloaders)

    #############################
    # 3. 数据存储部分
    result = {"feature": feature.numpy(), "label": data_label, "camera": camera_id, "index": pic_index}
    scipy.io.savemat(save_mat_dir, result)

# End


if __name__ == "__main__":
    test_dir = "../vid_pic"
    save_mat_dir = "./feature_result.mat"
    store_all_in_mat(test_dir, save_mat_dir)
