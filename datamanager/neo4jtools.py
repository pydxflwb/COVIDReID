from typing import Dict, List, Any, Union

from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
import json

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
#       接触关双向系仅连接目标关系
##########################
# 根据单条记录创建tid节点
def create_one_node(graph, pic_record, matcher):
    existnode = matcher.match(pic_record[1], trackID=pic_record[2],
                              starttime=int(pic_record[3].split("f")[1]),
                              endtime=int(pic_record[4].split("f")[1]))
    if not existnode:
        new_node = Node(pic_record[1], camera=pic_record[0], reID=pic_record[1], trackID=pic_record[2],
                        starttime=int(pic_record[3].split("f")[1]), endtime=int(pic_record[4].split("f")[1]),
                        path=pic_record[5], health=0)
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
            cnum +=1
    return cnum


def create_camera_relations(graph, cam_list):
    cr = 0
    for cam in cam_list:
        existc = graph.nodes.match("Camera", name=cam).all()
        existr = graph.nodes.match(camera=cam).all()
        for i in range(len(existr)):
            rel = graph.relationships.match(nodes={existc[0], existr[i]}, r_type="appear")
            if not rel:
                new_rel = Relationship(existc[0], "appear", existr[i], time=existr[i]["starttime"])
                graph.create(new_rel)
                cr += 1
    return cr


def create_same_relation_list(graph, reid):
    sr = 0
    existr = graph.nodes.match(reID=reid).order_by("_.starttime").all()
    for i in range(len(list(existr))-1):
        rel = graph.relationships.match(nodes={existr[i], existr[i+1]}, r_type="is_predecessor_of")
        if not rel:
            rel_pre = Relationship(existr[i], "is_predecessor_of", existr[i+1])
            rel_suc = Relationship(existr[i+1], "is_successor_of", existr[i])
            graph.create(rel_pre)
            graph.create(rel_suc)
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
            r0 = create_one_node(graph, record, matcher)    # 新创建文件的数量
            if r0:
                node_count += 1
        sr0 = create_same_relation_list(graph, record_list[0][1])
        sr1 += sr0
    c0 = create_cam_nodes(graph, cam_list)
    cr0 = create_camera_relations(graph, cam_list)

    print("#Neo4j#  Add " + str(node_count) + " Nodes and relevant " + str(sr1)+ " in File " + pic_json)
    print("#Neo4j#  Add " + str(c0) + " Camera Nodes and relevant " + str(cr0) + " Relationships in File " + pic_json)
    return node_count


# 从单条接触记录创建接触关系
def add_contact_relationship(graph, rel_record):
    # tid
    t1 = rel_record[0] + "t" + str(rel_record[1])
    t2 = rel_record[0] + "t" + str(rel_record[2])
    node1 = graph.nodes.match(trackID=t1).all()
    node2 = graph.nodes.match(trackID=t2).all()
    if node1 and node2 and (node1[0]["reID"] != node2[0]["reID"]):
        existrel = graph.relationships.match(nodes=[node1[0], node2[0]], r_type="contact")
        if not existrel:
            rel1to2 = Relationship(node1[0], "contact", node2[0], time=rel_record[3], cam=rel_record[0])
            rel2to1 = Relationship(node2[0], "contact", node1[0], time=rel_record[3], cam=rel_record[0])
            graph.create(rel1to2)
            graph.create(rel2to1)
            return True
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
            t_return = add_contact_relationship(graph, t)
            if t_return:
                rela_count += 1
    print('#Neo4j#  Add ' + str(rela_count) + " Relationships in File " + trackjson)
    return rela_count


def match_tool(graph, data, match_method):
    return_list = []

    # 输出格式 [长度，若干含属性的dict]
    # {'path': 'F:\\Competition\\covidreid\\static\\source\\reid_result\\1\\c1_p1_t1_f126.jpg',
    # 'trackID': 'c1t1', 'endtime': 246, 'health': 0, 'starttime': 126,
    # 'reID': '1', 'camera': 'c1'}
    if match_method == "by_cam":
        # data应该是camera，字符形式
        nodes = graph.nodes.match(camera=data).order_by("_.starttime").all()
        return_list.append(len(nodes))
        for i in range(len(nodes)):
            return_list.append(dict(nodes[i]))
        return return_list

    elif match_method == "by_reID":
        # data应该是reID(字符串)
        nodes = graph.nodes.match(reID=data).order_by("_.starttime").all()
        return_list.append(len(nodes))
        for i in range(len(nodes)):
            return_list.append(dict(nodes[i]))
        return return_list

    elif match_method == "by_contact":
        pass
    elif match_method == "by_attribute":
        pass
    elif match_method == "all":
        pass
    else:
        return 0

re = match_tool(graph0, "3", "by_reID")
print(re)


#
# if __name__ == "__main__":
#     reid_json = "../static/source/reid_data_for_neo4j.json"
#     contact_json = "../static/source/vid_json/contact.json"
#     n = create_nodes(graph0, reid_json, matcher0)
#     r = create_contact_relationships(graph0, contact_json)
#     print(n, r)

