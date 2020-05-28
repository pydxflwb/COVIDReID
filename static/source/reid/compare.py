import os, sys, json
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import scipy.io


def read_result_from_mat(mat_dir):
    result = scipy.io.loadmat(mat_dir)
    feature = torch.FloatTensor(result["feature"])
    label = result["label"][0]
    camera = result["camera"][0]
    index = result["index"][0]
    
    return feature, label, camera, index


def sort_img(f1, feas):
    feature = f1.cuda()
    feas = feas.cuda()
    query = feature.view(-1, 1)
    score = torch.mm(feas, query)
    score = score.squeeze(1).cpu()
    score = score.numpy()
    return score


def get_index(score):
    index = np.argsort(score)
    index = index[::-1]
    return index


def del_junk_index(i0, c0, index0, l0, s0):
    for j in range(len(index0)):
        # if l0[index0[j]] == l[i0+1]:
        #     return index0[j], 1
        if c0[index0[j]] != c0[i0+1]:
            if s0[index0[j]] > 0.60:
                return index0[j], s0[index0[j]]
            else:
                break
    if l0[index0[0]] == l[i0 + 1]:
        return index0[0], 1
    else:
        return index0[0], 0


def get_pic_sort(r_result):
    last_count = 1
    last = 1
    last_result = [0 for ii in range(len(r_result))]
    i = 0
    print(len(r_result))
    while i < len(r_result)-1:
        storage = [r_result[i]]
        for j in range(i+1, len(r_result)):   # 先找到所有同id图片
            if r_result[j][0] == r_result[i][0]:
                storage.append(r_result[j])
                if j == len(r_result)-1:
                    last = j
            else:
                last = j
                break
        print(storage)
        store_dic = {}
        for t in range(last-i):
            if storage[t][1][1] == 1:
                if i+t == 0:
                    last_result[0] = 1
                else:
                    last_result[i+t] = last_result[i+t-1]
            elif storage[t][1][1] == 0:
                last_count += 1
                last_result[i+t] = last_count
            else:
                if storage[t][2] not in store_dic.keys():   # 计数存入字典
                    store_dic[storage[t][2]] = storage[t][1][1]
                else:
                    store_dic[storage[t][2]] += storage[t][1][1]

        if store_dic:
            vmax = max(store_dic.values())
            vkey = 0
            vindex = 0
            for key, value in store_dic.items():
                if value == vmax:
                    vkey = key          # 找到最大概率的那个标签
                    break
            print(vkey)
            for st in r_result:
                if vkey == st[0]:
                    vindex = st[1][0]
                    print(vindex)
                    break
            for ti in range(i, last):
                last_result[ti] = last_result[vindex]

        i = last

    return last_result


if __name__ == "__main__":
    mat_dir = "./feature_result.mat"
    json_dir = "./reid_result.json"
    f, l, c, ind = read_result_from_mat(mat_dir)
    reid_result = []
    for i in range(0, len(f)-1):
        # print(i)
        s = sort_img(f[i+1], f[0:i+1])
        index = get_index(s)
        new_index = del_junk_index(i, c, index, l, s)
        ttt = [l[i+1], new_index, l[new_index[0]]]
        print(ttt)
        reid_result.append(ttt)
    lll = get_pic_sort(reid_result)
    with open(json_dir, "w") as f:
        f.write(json.dumps(lll))
    f.close()
