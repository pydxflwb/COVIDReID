import json
from typing import Any, Dict, List, Union

from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher

graph0 = Graph("http://localhost:7474", auth=("neo4j", "123456"))
matcher0 = NodeMatcher(graph0)


##########################
# neo4j数据库结构
# 节点类型：
#       场景camera, 入库方式：获得所有unique的camera
#       人——每个reid一个类，健康状况可以修改
#       相同reid不同tid之间，使用什么方法连接？建议双向链
#       接触关系仍不变，双向
##########################
# 关系类型：
#       camera-->pid节点，出现关系
#       同reid不同tid使用双向链表连接时间关系
#       接触双向关系仅连接前后继
##########################
# 根据单条记录创建tid节点
def create_one_node_old(graph, pic_record, matcher):
    existnode = matcher.match(pic_record[1], trackID=pic_record[2],
                              starttime=int(pic_record[3].split("f")[1]),
                              endtime=int(pic_record[4].split("f")[1]))
    if not existnode:
        attn = pic_record[5].split(".j")[0]
        attlist = attn.split('\\')
        attlist[5] = 'attribute_result'
        attdir = ""
        for a in range(len(attlist) - 1):
            attdir = attdir + attlist[a]
            attdir = attdir + '\\'
        attdir = attdir + attlist[-1] + ".json"
        attdir = ".." + attdir.split("covidreid")[1]
        attrresult = read_json_file(attdir)

        new_node = Node(pic_record[1], camera=pic_record[0], reID=pic_record[1], trackID=pic_record[2],
                        starttime=int(pic_record[3].split("f")[1]), endtime=int(pic_record[4].split("f")[1]),
                        path=pic_record[5], attributes=attrresult, health=0)
        graph.create(new_node)
        return True
    else:
        return False


# 新数据
# [
#  "c1",
#  "d0808",
#  "t0480",
#  "p01",
#  "r01",
#  "../static/source/reidresult/c1_d0808_t0480_p01_r01.jpg"
# ]
# Nodename, camera, reID, time, trackID, path, attribute, health
def create_one_node(graph, pic_record, matcher):
    nodename = str(int(pic_record[4].split("r")[-1]))
    time = pic_record[1].split("d")[-1] + pic_record[2].split("t")[-1]
    existnode = matcher.match(nodename, trackID=pic_record[0] + pic_record[3],
                              time=int(time)
                              )
    if not existnode:
        attn = pic_record[5].split(".j")[0]
        attlist = attn.split('reidresult')
        attdir = attlist[0] + "attributeresult" + attlist[1] + ".json"
        attrresult = read_json_file(attdir)

        new_node = Node(nodename, camera=pic_record[0], reID=pic_record[4], trackID=pic_record[0] + pic_record[3],
                        time=int(time), path=pic_record[5], attributes=attrresult, health=0)
        # print(new_node)
        graph.create(new_node)
        return True
    else:
        return False


def create_cam_nodes(graph, cam_list):
    cnum = 0
    for cam in cam_list:
        existc = graph.nodes.match("Camera", name=cam)
        if not existc:
            new_cnode = Node("Camera", name=cam)
            graph.create(new_cnode)
            cnum += 1
    return cnum


def create_camera_relations_old(graph, cam_list):
    cr = 0
    for cam in cam_list:
        existc = graph.nodes.match("Camera", name=cam).all()
        existr = graph.nodes.match(camera=cam).all()
        for i in range(len(existr)):
            rel = graph.relationships.match(
                nodes={existc[0], existr[i]}, r_type="appear")
            if not rel:
                new_rel = Relationship(
                    existc[0], "appear", existr[i], time=existr[i]["starttime"])
                graph.create(new_rel)
                cr += 1
    return cr


def create_camera_relations(graph, cam_list):
    cr = 0
    for cam in cam_list:
        existc = graph.nodes.match("Camera", name=cam).all()
        existr = graph.nodes.match(camera=cam).all()
        for i in range(len(existr)):
            rel = graph.relationships.match(
                nodes={existc[0], existr[i]}, r_type="appear")
            if not rel:
                new_rel = Relationship(
                    existc[0], "appear", existr[i], time=existr[i]["time"])
                graph.create(new_rel)
                cr += 1
    return cr


def create_same_relation_list_old(graph, reid):
    sr = 0
    existr = graph.nodes.match(reID=reid).order_by("_.starttime").all()
    for i in range(len(list(existr)) - 1):
        rel = graph.relationships.match(
            nodes={existr[i], existr[i + 1]}, r_type="is_predecessor_of")
        if not rel:
            rel_pre = Relationship(
                existr[i], "is_predecessor_of", existr[i + 1])
            rel_suc = Relationship(existr[i + 1], "is_successor_of", existr[i])
            graph.create(rel_pre)
            graph.create(rel_suc)
            sr += 1
    return sr


# 改成了单向关系
def create_same_relation_list(graph, reid):
    sr = 0
    # print(reid)
    existr = graph.nodes.match(reID=reid).order_by("_.time").all()
    # print(existr)
    for i in range(len(list(existr)) - 1):
        rel = graph.relationships.match(
            nodes={existr[i], existr[i + 1]}, r_type="is_predecessor_of")
        if not rel:
            rel_pre = Relationship(
                existr[i], "is_predecessor_of", existr[i + 1])
            graph.create(rel_pre)
            sr += 1
    return sr


# 根据整个reid文件创建tid节点和 camera节点
def create_nodes(graph, pic_json, matcher):
    with open(pic_json, "r") as f:
        pic_records = json.load(f)
    f.close()
    node_count = 0
    sr1 = 0
    cam_list = []
    for record_list in pic_records:
        for record in record_list:
            if record[0] not in cam_list:
                cam_list.append(record[0])
            r0 = create_one_node(graph, record, matcher)  # 新创建节点的数量
            if r0:
                node_count += 1
            sr0 = create_same_relation_list(graph, record[4])
            sr1 += sr0
    c0 = create_cam_nodes(graph, cam_list)
    cr0 = create_camera_relations(graph, cam_list)

    print("#Neo4j#  Add " + str(node_count) +
          " Nodes and relevant " + str(sr1) + " in File " + pic_json)
    print("#Neo4j#  Add " + str(c0) + " Camera Nodes and relevant " +
          str(cr0) + " Relationships in File " + pic_json)
    return node_count


# 属性json的读取
def read_json_file(filename):
    with open(filename, "r", encoding='UTF-8') as f:
        attributes = json.load(f)
    f.close()
    attrresult = []
    # print(attributes)
    mem = ""
    count = 0
    for key in attributes.keys():
        if attributes[key] >= 1:
            try:
                if key[0:2] == mem:
                    count += 1
                    if count <= 3:
                        attrresult.append(key)
                else:
                    count = 1
                    attrresult.append(key)
                mem = key[0:2]
            except IndexError:
                attrresult.append(key)
    return attrresult


# 从单条接触记录创建接触关系
def add_contact_relationship_old(graph, rel_record):
    # tid
    t1 = rel_record[0] + "t" + str(rel_record[1])
    t2 = rel_record[0] + "t" + str(rel_record[2])
    node1 = graph.nodes.match(trackID=t1).all()
    node2 = graph.nodes.match(trackID=t2).all()
    if node1 and node2 and (node1[0]["reID"] != node2[0]["reID"]):
        existrel = graph.relationships.match(
            nodes=[node1[0], node2[0]], r_type="contact")
        if not existrel:
            rel1to2 = Relationship(
                node1[0], "contact", node2[0], time=rel_record[3], cam=rel_record[0])
            rel2to1 = Relationship(
                node2[0], "contact", node1[0], time=rel_record[3], cam=rel_record[0])
            graph.create(rel1to2)
            graph.create(rel2to1)
            return True
        else:
            return False
    else:
        return False


def add_contact_relationship(graph, rel_record):
    # tid
    t1 = rel_record[0] + rel_record[1]
    t2 = rel_record[0] + rel_record[2]
    date = rel_record[3][0:4]
    print(date)
    node1 = graph.nodes.match(trackID=t1).all()
    node2 = graph.nodes.match(trackID=t2).all()
    if node1 and node2:
        for node in node1:
            date1 = str(node["time"]).zfill(8)
            if date1[0:4] == date:
                node01 = node
                break
        for node in node2:
            date2 = str(node["time"]).zfill(8)
            if date2[0:4] == date:
                node02 = node
                break
        if node01 and node02 and node01["reID"] != node02["reID"]:
            existrel = graph.relationships.match(
                nodes=[node01, node02], r_type="contact")
            if not existrel:
                rel1to2 = Relationship(
                    node01, "contact", node02, time=int(rel_record[3]), cam=rel_record[0])
                rel2to1 = Relationship(
                    node02, "contact", node01, time=int(rel_record[3]), cam=rel_record[0])
                graph.create(rel1to2)
                graph.create(rel2to1)
                return True
            else:
                return False
        else:
            return False
    else:
        return False


# 根据整个关系文件创建关系
def create_contact_relationships(graph, trackjson):
    with open(trackjson, "r") as f:
        trackdata = json.load(f)
    f.close()
    rela_count = 0
    for t_list in trackdata:
        for t in t_list:
            # print(t)
            t_return = add_contact_relationship(graph, t)
            if t_return:
                rela_count += 1
    print('#Neo4j#  Add ' + str(rela_count) +
          " Relationships in File " + trackjson)
    return rela_count


# 多种匹配模式的查询函数，用于列表界面
def match_tool(graph, data, match_method):
    return_list = []

    # 输出格式 [长度，若干含属性的dict]
    # {'path': 'F:\\Competition\\covidreid\\static\\source\\reid_result\\1\\c1_p1_t1_f126.jpg',
    # 'trackID': 'c1t1', 'endtime': 246, 'health': 0, 'starttime': 126,
    # 'reID': '1', 'camera': 'c1'}
    if match_method == "by_cam":
        # data应该是camera，字符形式
        nodes = graph.nodes.match(camera=data).order_by("_.time").all()
        return_list.append(len(nodes))
        for i in range(len(nodes)):
            return_list.append(dict(nodes[i]))
        return return_list

    elif match_method == "by_reID":
        # data应该是reID(字符串)
        data = "r" + str(data).zfill(2)
        nodes = graph.nodes.match(reID=data).order_by("_.time").all()
        return_list.append(len(nodes))
        for i in range(len(nodes)):
            return_list.append(dict(nodes[i]))
        return return_list

    elif match_method == "by_contact":
        pass
    elif match_method == "by_attribute":
        pass
    elif match_method == "all":
        nodes2 = graph.nodes.match(health=2).order_by("_.time").all()
        nodes1 = graph.nodes.match(health=1).order_by("_.time").all()
        nodes0 = graph.nodes.match(health=0).order_by("_.time").all()
        l = len(nodes2) + len(nodes1) + len(nodes0)
        return_list.append(l)
        for i in range(len(nodes2)):
            return_list.append(dict(nodes2[i]))
        for i in range(len(nodes1)):
            return_list.append(dict(nodes1[i]))
        for i in range(len(nodes0)):
            return_list.append(dict(nodes0[i]))
        return return_list
    else:
        return 0


# re = match_tool(graph0, "3", "by_reID")
# print(re)


# 收到健康状态修改表单后更改同步全数据库健康状态整体函数
def search_and_modify_health(graph, data):
    # data格式为[reID, health]

    # 修改为确诊
    if data[1] == 2:
        # 修改自己所有节点为确诊
        graph.run(
            "match (a{reID:'" + str(data[0]) + "'}) set a.health=2")
        # 修改当前健康的接触者为疑似
        graph.run(
            "match (a{reID:'" + str(data[0]) + "'})-[:contact]->(b{health:0}) match (c{reID:b.reID}) set "
                                               "c.health=1")
    # 修改为疑似
    elif data[1] == 1:
        # 只对健康的人修改为疑似
        graph.run(
            "match (a{reID:'" + str(data[0]) + "', health:0}) set a.health=1")
    # 修改为健康
    else:
        a = graph.run("match (a{reID:'" + str(data[0]) + "'}) return a.health").data()
        h = a[0]['a.health']
        if h != 2:
            graph.run("match (a{reID:'" + str(data[0]) + "'}) set a.health=0")
        else:
            graph.run("match (a{reID:'" + str(data[0]) + "'})-[:contact]->(b{health:1}) match (c{reID:b.reID}) set "
                                                         "c.health=0")
            graph.run("match (a{reID:'" + str(data[0]) + "'}) set a.health=0")
    return 1


# 带属性的行人列表导出函数


def get_human_list_old(graph, h):
    result = []
    nodes = graph.nodes.match(health=h).order_by("_.starttime").all()
    for i in range(len(nodes)):
        result.append(dict(nodes[i]))


def get_human_list(graph, h):
    result = []
    nodes = graph.nodes.match(health=h).order_by("_.time").all()
    for i in range(len(nodes)):
        result.append(dict(nodes[i]))


# echart数据导出函数
def update_json_data(graph, date):
    # echart要求输出的几个数据：
    date0 = int(date) * 10000
    h_num = graph.run("MATCH (n{health:0}) WHERE 0< n['time']-" + str(date0) + " < 10000 RETURN count(labels(n))")
    h_num = list(h_num)
    h_num = h_num[0].values()[0]
    h_num = int(h_num)
    s_num = graph.run("MATCH (n{health:1}) WHERE 0< n['time']-" + str(date0) + " < 10000 RETURN count(labels(n))")
    s_num = list(s_num)
    s_num = s_num[0].values()[0]
    s_num = int(s_num)
    a_num = graph.run("MATCH (n{health:2}) WHERE 0< n['time']-" + str(date0) + " < 10000 RETURN count(labels(n))")
    a_num = list(a_num)
    a_num = a_num[0].values()[0]
    a_num = int(a_num)
    return h_num, s_num, a_num

# 对单个节点更改健康属性的原子化操作
# def modify_health_of_node(node0, value):
#     if node0["health"] != value:
#         node0["health"] = value
#     return 1
# update_json_data(graph0)
# search_and_modify_health(graph0, ["3", 0])
#


# if __name__ == "__main__":
#     reid_json = "../static/source/new_result_for_neo4j.json"
#     contact_json = "../static/source/new_contact.json"
#     # n = create_nodes(graph0, reid_json, matcher0)
#     # print(n)
#     r = create_contact_relationships(graph0, contact_json)
#     print(r)
