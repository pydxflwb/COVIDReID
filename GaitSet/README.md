# 步态识别部分

主要使用GaitSet算法，在CASIA-B数据集上进行训练

## 代码修改部分

1. 修改 config.py 文件内的部分配置参数
2. pretreatment.py 文件内的图像存储函数更换为 cv2.imwrite()

## 训练与测试

直接运行 train.py 和 test.py 文件即可

## 提取特征向量

样例代码：

```python
from extract_feature import GetFeature

# initialize GetFeature
get_feature = GetFeature(
    encoder_path="./work/checkpoint/GaitSet/GaitSet_CASIA-B_73_False_256_0.2_128_full_30-80000-encoder.ptm")

# set the path of sihouettes
silhouettes_path = "PATH_OF_SILHOUETTES"

# extract_feature function will preprocess first 
# and then extract the gait feature of the set of sihouettes
feature = get_feature.extract_feature(silhouettes_path=silhouettes_path)
```