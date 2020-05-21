from py2neo import Graph, Node, Relationship
graph0 = Graph("http://localhost:7474", auth=("neo4j", "123456"))


# 从单条图片记录创建节点
def create_one_node(graph, pic_record):
    new_node = Node("Person", reID=pic_record.reID, trackID=pic_record.trackID,
                    time=pic_record.time, camera=pic_record.cam, health=0)
    graph.create(new_node)


# 从单条接触记录创建关系
def add_relationship(graph, rel_record):
    node1 = graph.nodes.match(trackID=rel_record.trackID1).first()
    node2 = graph.nodes.match(trackID=rel_record.trackID2).first()
    rel1to2 = Relationship(node1, "contact", node2,
                           time=rel_record.time, cam=rel_record.cam)
    graph.create(rel1to2)


# 根据整个节点文件创建节点
def create_nodes(graph, pic_records):
    for record in pic_records:
        add_relationship(graph, record)

# 根据整个关系文件创建关系
def create_relationships(graph, )


# 查找处理
def return_from_database():
    pass
