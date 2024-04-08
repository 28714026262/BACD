from WebFSM import FSM

class UserGroup:
    def __init__(self) -> None:
        self.fsm = ""
        self.groupName = ""
        self.priority = -1


class FSMAnalysis:
    def __init__(self) -> None:
        self.UserGrouplist = []
    
    def VerticalBACDetected(self):
        pass

    def HorizontalBACDetected(self):
        pass

    def diffFSM(self, FSM1, FSM2):
        # find diff node
        # get diff node connection and diff node interface
        # find same node diff interface
        return 0 # [node:[action,],]

    def childgraphfinder(self, FSM_input):
        res_fsm = None
        return res_fsm
    
    def long_bussiness_chain(self, FSM_input):
        return None # [node:[action],]
        
    def global_share_area(self, FSM_input):
        res_fsm = None
        # find same node
        # 是否执行无权限爬虫
        # - 执行
        # - 不执行
        return res_fsm

    def NoAuthSpider(self):
        pass

    def cutEdgeFromEDGENODEToShareGraph(self, FSM_input):
        pass

    def EDGENODEFinder(self, FSM_input):
        return None # [node_list]
    
    # gpt answer
def topological_sort(graph):
    # 初始化入度为0的节点队列
    indegree_zero = []
    for node in graph:
        if graph[node]['indegree'] == 0:
            indegree_zero.append(node)

    # 拓扑排序结果
    topological_order = []

    while indegree_zero:
        node = indegree_zero.pop(0)
        topological_order.append(node)

        # 更新相邻节点的入度
        for neighbor in graph[node]['neighbors']:
            graph[neighbor]['indegree'] -= 1
            if graph[neighbor]['indegree'] == 0:
                indegree_zero.append(neighbor)

    return topological_order

def diff(graph, node_values, topological_order):
    # 构建差分数组
    diff_array = [0] * len(node_values)
    for i, node in enumerate(topological_order):
        diff_array[i] = node_values[node]

    # 更新差分数组
    for node in topological_order:
        for neighbor in graph[node]['neighbors']:
            diff_array[topological_order.index(neighbor)] -= diff_array[topological_order.index(node)]

    return diff_array

# 示例图结构
graph = {
    'A': {'neighbors': ['B', 'C'], 'indegree': 0},
    'B': {'neighbors': ['C', 'D'], 'indegree': 1},
    'C': {'neighbors': ['D'], 'indegree': 2},
    'D': {'neighbors': [], 'indegree': 2}
}

# 节点值
node_values = {
    'A': 5,
    'B': 3,
    'C': 7,
    'D': 4
}

# 拓扑排序
topological_order = topological_sort(graph)

# 计算差分数组
diff_array = diff(graph, node_values, topological_order)

print("拓扑排序结果:", topological_order)
print("差分数组:", diff_array)   


import networkx as nx

# 创建示例图形
G1 = nx.Graph()
G1.add_edges_from([(1, 2), (2, 3), (3, 4)])

G2 = nx.Graph()
G2.add_edges_from([(1, 2), (1, 3), (2, 3)])

G3 = nx.Graph()
G3.add_edges_from([(1, 2), (2, 3), (3, 5)])

# 找到共有节点
common_nodes = set(G1.nodes())  # 先假设第一个图的节点集合为共有节点集合
for graph in [G2, G3]:
    common_nodes = common_nodes.intersection(graph.nodes())

# 找到共有边
common_edges = []
for edge in G1.edges():
    if all(node in common_nodes for node in edge):
        common_edges.append(edge)

# 构建共有图
common_graph = nx.Graph()
common_graph.add_nodes_from(common_nodes)
common_graph.add_edges_from(common_edges)

print("共有节点：", common_nodes)
print("共有边：", common_edges)