import os, sys, json
from shutil import copyfile
import torch
import torch.nn as nn
from torchvision import datasets, transforms


def re_classify(test_dir, json_dir, save_dir):
    with open(json_dir, "r") as f:
        result = json.load(f)
    f.close()
    result[-1] = result[-2]
    result.insert(0, 1)
    data_dir = test_dir
    image_datasets = datasets.ImageFolder(data_dir)
    data_path = image_datasets.imgs
    
    for i in range(len(data_path)):
        newdir = save_dir+"/"+str(result[i])+"/"
        if not os.path.exists(newdir):
            os.mkdir(newdir)
        oldpath =  data_path[i][0]
        filename = os.path.basename(oldpath)
        newpath = newdir+filename
        copyfile(oldpath, newpath)
        



if __name__ == "__main__":
    test_dir = "../vid_pic"
    json_dir = "./reid_result.json"
    save_dir = "../reid_result"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    re_classify(test_dir,json_dir, save_dir)
