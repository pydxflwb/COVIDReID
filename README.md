# CovidReid 校园COVID19接触人员智能排查系统
* CISCN2020 作品赛 一等奖 参赛作品

## 系统组成
* 在以下相关算法基础上进行改进:
  * 步态识别: [GaitSet](https://github.com/AbnerHqC/GaitSet)
  * 行人换装再识别: [DG-Net](https://github.com/NVlabs/DG-Net), [reID-baseline](https://github.com/layumi/Person_reID_baseline_pytorch)
  * 行人属性识别: [pedestrian-attribute-recognition](https://github.com/dangweili/pedestrian-attribute-recognition-pytorch)
  * 行人目标识别与跟踪:[CenterTrack](https://github.com/xingyizhou/CenterTrack), [Mask-RCNN](https://github.com/facebookresearch/maskrcnn-benchmark)
* 使用数据库: neo4j v4

## 使用
* 由于某些细节实现工作量和时间问题，本系统部分数据细节暂时未在Github公开。如有需要了解系统更多细节或实装使用，请联系pydxflwb@sjtu.edu.cn

1. Clone Github代码
2. 下载static数据:[BaiduNetDisk](https://pan.baidu.com/s/1N6QTbW30bO3i74IGh6KpXg) 提取码:k8nu
3. 解压到source_code文件夹下
4. 运行环境:
  * Python 3(推荐3.5-3.7), 
  * __Django v2.2__(重要！3.0的特性改动可能导致不能兼容！)
  * neo4j Community v4 + py2neo v5(请务必安装匹配版本！__neo4j v3 == py2neo v4__, __neo4j v4 == py2neo v5__, neo4j v4的内核改动导致大版本__不匹配完全无法使用__！)
5. (对应文件夹下)python修改 source_code/datamanager/neo4jtools.py下的最后注释（if __name__ == "__main__"后的所有内容），取消该段注释并运行neo4jtools.py进行数据入库。
__注意__:请确保neo4j服务处于启动状态。 datamanager/view.py中可以修改neo4j数据库连接的用户和密码，请注意修改。
对第5步可能出现的改动和问题，请联系pydxflwb@sjtu.edu.cn或提出issues
6. python manage.py runserver启动系统网页，登录(admin, 123456)
 
7. *Extra* 除了网页系统还想运行一下其它算法，了解系统更多原理:
  * 下载 [部分算法](https://pan.baidu.com/s/1-6fIYjbHywIhcb4snNfc9w)  提取码:2hzi
  * 参考部分static文件夹数据夹中的代码
  * 其它算法参考“系统组成”一节提到的算法
  * 更多问题请联系pydxflwb@sjtu.edu.cn，或提出issues

## Info 

作者：
  * [肖 鹏宇](github.com/pydxflwb) (owner of this repo)
  * [曹 昊天](github.com/caohaotiantian)
  * [袁 鑫](https://github.com/yx3266) 
  * [兰 焜耀](https://github.com/lankunyao)
上海交通大学 网络空间安全学院
