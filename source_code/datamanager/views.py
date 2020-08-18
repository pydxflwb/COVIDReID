import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datamanager.neo4jtools import *
from http.server import BaseHTTPRequestHandler, HTTPServer
from py2neo import Graph, Node, Relationship

# graph0 = Graph("http://localhost:7474", auth=("neo4j", "123456"))

healthlist = ["健康", "疑似", "确诊"]


# Create your views here.


def return_datalist(request):
    pass


def neo4j(request):
    return render(request, "neo4j.html")


def statistics(request):
    return render(request, "statistics.html")


def map(request):
    return render(request, "map.html")


def get_data_from_nodes(nodes):
    data = []
    len = nodes[0]
    for i in range(len):
        data0 = get_data_from_node(nodes[i + 1])
        data.append(data0)
    return data


def get_data_from_node(node):
    pdata = []
    pdata.append(node["reID"])

    path = node["path"].split("static")[1]
    path = path[1:]
    # pathlist = path.split("\\")
    # pathnew = ""
    # for p in range(1, len(pathlist) - 1):
    #     pathnew = pathnew + pathlist[p]
    #     pathnew = pathnew + "/"
    # pathnew += pathlist[-1]
    pdata.append(path)

    pdata.append(node["camera"])

    time = str(node["time"]).zfill(8)
    mon = int(time[0:2])
    day = int(time[2:4])
    # print(mon, day)
    time0 = int(time[4:])
    videotime = datetime.datetime(2020, mon, day, 10, 0, 0)
    time = videotime + datetime.timedelta(seconds=int(time0 / 30))
    pdata.append(time.strftime("%Y-%m-%d %H:%M:%S"))

    pdata.append(node["attributes"])
    pdata.append(healthlist[int(node["health"])])
    pdata.append(node["trackID"])
    # print(pdata)

    return pdata


# 有待修改
def get_welcome_data(request):
    # 查询每天的人员数量，这里需要后端来配合
    h1,s1,a1 = update_json_data(graph0, 808)
    h2,s2,a2 = update_json_data(graph0, 809)
    h3,s3,a3 = update_json_data(graph0, 810)

    healthy = ["健康", 0, 0, h1, h2, h3, 0, 0]
    confirmed = ["确诊", 0, 0, a1, a2, a3, 0, 0]
    suspected = ["疑似", 0, 0, s1, s2, s3, 0, 0]
    # 查询每天新增的人员数量，这里需要后端配合
    healthy_added = ["健康新增", 0, 0, h1, h2, h3, 0, 0]
    confirmed_added = ["确诊新增", 0, 0, a1, a2, a3, 0, 0]
    suspected_added = ["疑似新增", 0, 0, s1, s2, s3, 0, 0]
    # 组合成需要的数据形式
    data = {
        "health_ratio_pie": [{
            "name": "健康",
            "value": sum(healthy[1:])
        }, {
            "name": "确诊",
            "value": sum(confirmed[1:])
        }, {
            "name": "疑似",
            "value": sum(suspected[1:])
        }],
        "health_pie_line_combine":
            [["日期", "8.06", "8.07", "8.08", "8.09", "8.10", "8.11", "8.12"], healthy, confirmed,
             suspected],
        "new_added_data": [healthy_added, confirmed_added, suspected_added]
    }
    return HttpResponse(json.dumps(data))


# 连接数据库查询
def get_human_features(person, camera):
    print(person)
    print(camera)
    if person:
        print(1)
        mdata = person
        method = "by_reID"
    elif camera and camera != "0":
        mdata = "c" + camera
        method = "by_cam"
    else:
        print(3)
        mdata = ""
        method = "all"
    nodes = match_tool(graph0, mdata, method)
    data = get_data_from_nodes(nodes)
    # data = [
    #     [
    #         '2005260001',
    #         'images/person1.png',
    #         '2020/05/26 15:48:45',
    #         '监控点1',
    #         ['男性', '灰色上衣', '黑色短裤', '未佩戴饰品'],
    #         '健康'
    #     ],
    #     [
    #         '2005260021',
    #         'images/person1.png',
    #         '2020/05/26 15:48:45',
    #         '监控点2',
    #         ['男性', '灰色上衣', '黑色短裤', '未佩戴饰品'],
    #         '健康'
    #     ]
    # ]
    return data


# 这里需要连接数据库进行查询，查询代码我没写，只是给个例子
# 通过查询 id 查询行人属性
def get_this_person_features(id):
    data = [id, ['男性', '灰色上衣', '黑色短裤', '未佩戴饰品'], '健康']
    return data


def human_feature(request):
    if request.POST:
        person = request.POST["start"]
        camera = request.POST["place"]
    else:
        person = ""
        camera = ""
    human_features = get_human_features(person, camera)
    return render(request, "human_feature.html", {'people': human_features})


@csrf_exempt
def update_health(request):
    if request.POST:
        id = request.POST.get('id')
        health = request.POST.get('type')
        # print(id, health)
        data1 = [str(id), int(health)]
        flag = search_and_modify_health(graph0, data1)
        print(flag)
    human_features = get_human_features("", "")
    return render(request, "human_feature.html", {'people': human_features})


def human_edit(request):
    # 获取 id
    id = request.GET['id']
    data = get_this_person_features(id)
    features = ''
    for i in data[1]:
        features += i
        features += ';'
    data[1] = features
    return render(request, "human_edit.html", {'person': data})


# 查看行人图片
def gait_detail(request):
    img_src = request.GET.get('src')
    return render(request, "gait_detail.html", {'img': img_src})


def healthy_table(request):
    return render(request, "healthy_table.html")


def confirmed_table(request):
    return render(request, "confirmed_table.html")


def suspected_table(request):
    return render(request, "suspected_table.html")


def get_healthy_data(request):
    # attributes, reID, time = graph0.run("match(n) where n.health=0 return n.attributes,n.reID,n.time")
    data = graph0.run(
        "match(n) where n.health=0 return n.attributes,n.reID,n.time").data()
    result = {
        "reID": [],
        "attributes": [],
        "time": []
    }
    for i in data:
        result["reID"].append(i['n.reID'])
        result["attributes"].append(",".join(i['n.attributes']))
        result["time"].append(i['n.time'])

    return HttpResponse(json.dumps(result))


def get_suspected_data(request):
    # attributes, reID, time = graph0.run("match(n) where n.health=0 return n.attributes,n.reID,n.time")
    data = graph0.run(
        "match(n) where n.health=1 return n.attributes,n.reID,n.time").data()
    result = {
        "reID": [],
        "attributes": [],
        "time": []
    }
    for i in data:
        result["reID"].append(i['n.reID'])
        result["attributes"].append(",".join(i['n.attributes']))
        result["time"].append(i['n.time'])

    return HttpResponse(json.dumps(result))


def get_confirmed_data(request):
    # attributes, reID, time = graph0.run("match(n) where n.health=0 return n.attributes,n.reID,n.time")
    data = graph0.run(
        "match(n) where n.health=2 return n.attributes,n.reID,n.time").data()
    result = {
        "reID": [],
        "attributes": [],
        "time": []
    }
    for i in data:
        result["reID"].append(i['n.reID'])
        result["attributes"].append(",".join(i['n.attributes']))
        result["time"].append(i['n.time'])

    return HttpResponse(json.dumps(result))
