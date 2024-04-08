import sys
import os
import copy
from WebFlow import GFNA, FlowNode, GWF, FlowSet
from Tools.RequestsAnalyser.HTMLRequestAnalyzer.HTMLRequestAnalyzer import *
from Tools.configloader import *
# from Tools.Enumeration import *
from Tools.Chrome_Log_Preprocess import *

# 制图用
import networkx as nx
import matplotlib.pyplot as plt

#把node底下的action装成一个container
class RequestWithResponse:
    def __init__(self) -> None:
        self.URL = ""
        self.method = ""
        self.status = ""
        self.header = {}
        self.params_get = {}
        self.params_post = {}
        self.param_body = ""
        #self.cookies = {}
        self.response_text = ""
        self.response = HTMLResponse()

    def setFromFlowNode(self, url, flow_node: FlowNode):
        self.URL = copy.deepcopy(url)
        self.method = copy.deepcopy(flow_node.method)
        self.status = copy.deepcopy(flow_node.status)
        self.header = copy.deepcopy(flow_node.header)
        self.params_get = copy.deepcopy(flow_node.params_get)
        self.params_post = copy.deepcopy(flow_node.params_post)
        self.param_body = copy.deepcopy(flow_node.param_body)
        #self.cookies = copy.deepcopy(flow_node.cookies)
        self.response_text = copy.deepcopy(flow_node.response_text)
        self.response.deepcopy(flow_node.response)

    def deepcopy(self, new_Req_Resp):
        self.URL = copy.deepcopy(new_Req_Resp.URL)
        self.method = copy.deepcopy(new_Req_Resp.method)
        self.status = new_Req_Resp.status
        self.header = copy.deepcopy(new_Req_Resp.header)
        self.params_get = copy.deepcopy(new_Req_Resp.params_get)
        self.params_post = copy.deepcopy(new_Req_Resp.params_post)
        self.param_body = copy.deepcopy(new_Req_Resp.param_body)
        #self.cookies = copy.deepcopy(new_Req_Resp.cookies)
        self.response_text = copy.deepcopy(new_Req_Resp.response_text)
        self.response.deepcopy(new_Req_Resp.response)

    def is_same_requset(self, input_req_and_resp):
        temp_flag, domain = GWF.is_Same_URL_Route(self.URL, input_req_and_resp.URL)
        if not temp_flag:
            return False
        if self.method != input_req_and_resp.method:
            return False
        # 由于header的内容很多有浏览器生成实现，因此这里不作为相似请求响应的结果。
        # for key in self.header:
        #     return False
        if self.method.upper == "GET":
            if len(self.params_get) > len(input_req_and_resp.params_get):
                for key in input_req_and_resp.params_get:
                    if key not in self.params_get:
                        return False
            else:
                for key in self.params_get:
                    if key not in input_req_and_resp.params_get:
                        return False
        elif self.method.upper == "POST":
            for key in self.params_post:
                if key not in input_req_and_resp.params_post:
                    return False
        # cookie也是一个可能会发生改变但不影响request功能的内容
        # if self.cookies:
        #     return False
        return True

    def is_same_response(self, input_response):
        pass


class Action:
    def __init__(self) -> None:
        self.isAction = 1  # 1 is normal Action, and 2 is Connection
        self.ActionType = -1 # 1 is Tab Switch, 2 is URL Change, 3 is Click, 4 is Input
        self.key_num_action = -1
        self.role = ""
        self.src_node_key = ""
        self.req_list = []

        # 考虑对相似行为分析时提供一些冗余度
        self.similarity_redundancy = 1.00

        self.Type = -1

    def add_Res_and_Resp(self, new_request_and_response):
        temp_RR = RequestWithResponse()
        temp_RR.deepcopy(new_request_and_response)
        self.req_list.append(temp_RR)

    def deepcopy(self, newAction):
        self.isAction = newAction.isAction
        self.key_num_action = newAction.key_num_action
        self.role = copy.deepcopy(newAction.role)
        self.src_node_key = newAction.src_node_key
        self.req_list = copy.deepcopy(newAction.req_list)

    # def action_type_speculate(self):
    #     # condition1
    #     self.Type = FSM_ACTION_TYPE_ADD
    #     # condition2
    #     self.Type = FSM_ACTION_TYPE_DELETE
    #     # condition3
    #     self.Type = FSM_ACTION_TYPE_EDIT
    #     # condition4
    #     self.Type = FSM_ACTION_TYPE_READ

    def boundaryAnalysis(self):
        # 前边界对齐
        pass

        # 后边界对齐

    def is_same_param_exist(self, single_request, request_list):
        # 不在意request
        pass

    def get_request_list_param(self, request_list):
        get_param = {}
        post_param = {}
        for req in request_list:
            pass

    def isSameAction(self, anotherAction) -> bool:
        if self.src_node_key != anotherAction.src_node_key:
            return False
        len_self = len(self.req_list)
        len_another = len(anotherAction.req_list)
        iter_self = 0
        iter_another = 0
        has_different_req_flag = False
        # - 先查找first_req
        # for iter_self in range(len_self):
        #     for iter_another in range(len_another):
        #         same_flag = self.req_list[iter_self].is_same_request(anotherAction.req_list[iter_another])
        #         if same_flag:
        #             first_req_founded_flag = True
        #             break
        # if not first_req_founded_flag:
        #     return False

        # 再按照first req进行遍历
        # iter_self = iter_self + 1
        # iter_another = iter_another + 1
        # same_flag = self.req_list[iter_self].is_same_request(anotherAction.req_list[iter_another])
        # if not same_flag:
        #     pass
        # - 不查找first_req
        if len_self != len_another:
            return False
        for iter_self in range(len_self):
            same_flag = self.req_list[iter_self].is_same_request(anotherAction.req_list[iter_self])
            if not same_flag:
                return False
        return True
        # 此处要考虑是否存在中间多余req，但这些req要首先考虑
        # for iter_1 in range(len_self) - iter_self:
        #     for iter_2 in range(len_another) - iter_another:
        #         same_flag = self.req_list[iter_self + 1 + iter_1].is_same_request(anotherAction.req_list[iter_another + 1 + iter_2])


class Connection(Action):
    def __init__(self) -> None:
        super(Connection, self).__init__()
        self.isAction = 2  # 1 is normal Action, and 2 is Connection
        self.dest_node_key = ""

    def deepcopy(self, newConnection):
        self.isAction = newConnection.isAction
        self.key_num_action = newConnection.key_num_action
        self.role = copy.deepcopy(newConnection.role)
        self.src_node_key = newConnection.src_node_key
        self.req_list = copy.deepcopy(newConnection.req_list)
        self.dest_node_key = newConnection.src_node_key


class Node:
    def __init__(self) -> None:
        self.Role = ""

        self.URL = ""
        self.URL_list = []
        self.URL_param = {}
        self.WebSourceCodePath = ""
        self.action_map_from_self_node = {}
        self.connection_map_from_self_node = {}

    def set(self,
            _role_name,
            _url,
            _url_list,
            _url_param,
            _web_source_code_path) -> None:
        # function will both recieve the normal action and the connection
        self.Role = _role_name
        self.URL = _url
        self.URL_list = copy.deepcopy(_url_list)
        self.URL_param = copy.deepcopy(_url_param)
        self.WebSourceCodePath = _web_source_code_path

    def isSameNode(self, another_node):
        same_flag = True
        if self.URL == another_node:
            same_flag = False
        self_keys_set = set(list(self.URL_param.keys()))
        another_keys_set = set(list(another_node.URL_param.keys()))
        if not bool(self_keys_set.intersection(another_keys_set)):
            same_flag = False
        if self.WebSourceCodePath != "" and another_node.WebSourceCodePath != "":
            if not self.HTML_Similarity_Check(self.WebSourceCodePath, another_node.WebSourceCodePath):
                same_flag = False
        return same_flag

    def HTML_Similarity_Check(self, self_source_code_path, another_source_code_path) -> bool:
        same_flag = True
        return same_flag

class BaseFSM:
    def __init__(self) -> None:
        self.NodeSet = {}
        self.Action = {}
        self.Connection = {}

class FSM(BaseFSM):
    def __init__(self) -> None:
        self.NodeSet = {}
        self.Action = {}
        self.Connection = {}
        self.Role = ""
        self.Role_key_num = -1

        self.req_node_refer = {}
        self.url_node_refer = []
        self.gap_node_refer = {}
        self.connection_node_refer = {}
        self.flow_list_with_gap ={}

    #每一次装在一个role
    def LoadWebFlowSet(self):
        self.Role = GFNA.g_flow_role_group_container.role_name
        for i in GFNA.g_flow_role_group_container.flowset.FlowsetContainer:
            self.req_node_refer = i.req_node_refer
            self.url_node_refer = i.url_node_refer
            self.gap_node_refer = i.gap_node_refer
            self.connection_node_refer = i.connection_node_refer
            self.flow_list_with_gap = i.flow_list_with_gap
            self.LoadContainer()
            # try:
            #     print(self.Role)
            #     print(self.req_node_refer)
            #     print(self.url_node_refer)
            #     print(self.gap_node_refer)
            #     print(self.connection_node_refer)
            #     print(self.flow_list_with_gap)
            # except:
            #     print("Load Data Error")

    #装载log分析得到的 gap_list 和 flow_with_gap
    #flow_with_gap->[start_req, end_req, action_node_num, sequence_num]
    def LoadContainer(self):
        # 对node和action进行装载
        for url_node, list in self.flow_list_with_gap.items():
            route_list, url_param = GWF.get_URL_Route(url_node)
            current_node_key_node = self.get_node_by_route_list(route_list)
            if current_node_key_node == -1:
                localNode = Node()
                localNode.set(
                    _role_name="",
                    _url=url_node,
                    _url_list=route_list,
                    _url_param = url_param,
                    _web_source_code_path = ""
                )
                self.NodeSet[url_node] = localNode
            #对action和connection进行装载
            for req_seq in list:
                if req_seq[2] in self.connection_node_refer.keys():
                    self.getAction(self.connection_node_refer[req_seq[2]], req_seq[2], [req_seq[0], req_seq[1]])
                else:
                    self.getAction(url_node, req_seq[2], [req_seq[0], req_seq[1]])

    def getAction(self, url_node, key_num, req_list):
        if isinstance(url_node, list):
            temp_action = Connection()
            temp_action.isAction = 2  # 1 is normal Action, and 2 is Connection
            temp_action.ActionType = self.gap_node_refer[key_num].gap_type
            temp_action.key_num_action = key_num
            temp_action.role = self.Role
            temp_action.src_node_key = url_node[0]
            temp_action.dest_node_key = url_node[1]

            start_loading = False
            for request_node in self.req_node_refer.keys():
                if request_node == req_list[0]:
                    start_loading = True
                if start_loading == True:
                    r_r_container = RequestWithResponse()
                    # 若是NoneType报错，则跳过
                    try:
                        # 目前没对cookie做分析
                        r_r_container.setFromFlowNode(self.NodeSet[url_node[0]].URL, self.req_node_refer[request_node])
                        temp_action.add_Res_and_Resp(r_r_container)
                    except:
                        print(f"connection_req_node {request_node} is a NoneType, will not process")
                        continue
                if request_node == req_list[1]:
                    break
            # connection也当作action供生成图用
            self.NodeSet[url_node[0]].action_map_from_self_node[key_num] = temp_action
            # 生成图的edge用
            self.NodeSet[url_node[0]].connection_map_from_self_node[key_num] = temp_action
        else:
            temp_action = Action()
            temp_action.isAction = 1  # 1 is normal Action, and 2 is Connection
            temp_action.ActionType = self.gap_node_refer[key_num].gap_type
            temp_action.key_num_action = key_num
            temp_action.role = self.Role
            temp_action.src_node_key = url_node
            #若action不造成req resp则直接等于[]
            if req_list[0] == -1 and req_list[1] == -1:
                self.NodeSet[url_node].action_map_from_self_node[key_num] = []
            else:
                #若有则进行分析
                start_loading = False
                for request_node in self.req_node_refer.keys():
                    if request_node == req_list[0]:
                        start_loading = True
                    if start_loading == True:
                        r_r_container = RequestWithResponse()
                        #若是NoneType报错，则跳过
                        try:
                            # 目前没对cookie做分析
                            r_r_container.setFromFlowNode(self.NodeSet[url_node].URL, self.req_node_refer[request_node])
                            temp_action.add_Res_and_Resp(r_r_container)
                        except:
                            print(f"action_req_node {request_node} is a NoneType, will not process")
                            continue
                    if request_node == req_list[1]:
                        break
                self.NodeSet[url_node].action_map_from_self_node[key_num] = temp_action

    def get_node_by_route_list(self, url_list) -> int:
        # for node_key_num in self.NodeSet:
        #     if url == self.NodeSet[node_key_num].URL:
        #         return node_key_num
        # return -1
        for node_key_num in self.NodeSet:
            flag, domain_name_useless = GWF.is_Same_URL_Route_by_list(url_list, self.NodeSet[node_key_num].URL_list)
            if flag:
                return node_key_num
        return -1

    #WebFlow已经处理了SameNode，个人感觉可以直接运用flow_with_gap的信息
    def haveSameNode(self):
        pass


class RoleContainer:
    def __init__(self) -> None:
        pass


GFSM = FSM()

class FSMGraph:
    def __init__(self):
        self.FSM = GFSM
        self.NodeSet = {}
        self.Role = ""
        self.NodeContainer = {}
        self.EdgeContainer = {}
        self.WeightContainer = {}
        self.gap_node_refer = {}

    def load_graph(self):
        self.FSM.LoadWebFlowSet()
        self.Role = self.FSM.Role
        self.NodeSet = self.FSM.NodeSet
        self.gap_node_refer = self.FSM.gap_node_refer
        count = 0

        for url_node, action in self.NodeSet.items():
            # Node Container装载：StartURL->ActionNodeContainer
            # for node_num, action_node in action.action_map_from_self_node.items():
                # 结点太多了这里只装载url_list
                # if url_node not in self.NodeContainer:
                #     self.NodeContainer[url_node] = []
                # else:
                #     self.NodeContainer[url_node].append(node_num)
                # self.NodeContainer.append(url_node)

            self.NodeContainer[url_node] = f"Action Container {count + 1}"
            count += 1
            # Edge Container装载：SingleActionNode->NextURL
            for node_num, url_list in action.connection_map_from_self_node.items():
                if self.gap_node_refer[node_num].gap_type == 1:
                    self.WeightContainer[node_num] = "TAB SWITCH"
                elif self.gap_node_refer[node_num].gap_type == 2:
                    self.WeightContainer[node_num] = "ACTIVATED URL"
                elif self.gap_node_refer[node_num].gap_type == 3:
                    self.WeightContainer[node_num] = f"CLICKED AT {self.gap_node_refer[node_num].click_element.className}"
                elif self.gap_node_refer[node_num].gap_type == 4:
                    self.WeightContainer[node_num] = f"INPUT AT {self.gap_node_refer[node_num].input_element.className}"
                else:
                    continue
                self.EdgeContainer[node_num] = [url_list.src_node_key, url_list.dest_node_key]

        print("Node Container: ", self.NodeContainer)
        print("Edge Container: ", self.EdgeContainer)
        print("Weight Container: ", self.WeightContainer)

        self.create_graph()

    def create_graph(self):
        G = nx.DiGraph()

        for url, container in self.NodeContainer.items():
            G.add_node(url)
            G.add_node(container)
            G.add_edge(url, container, weight="STORES ACTION")

        for node, urls in self.EdgeContainer.items():
            if len(urls) == 2:
                G.add_edge(urls[0], urls[1], weight=self.WeightContainer[node])

        # G.add_edge("http://29.20.130.39:31001/?SSO_loginName=amlhbmdzdXlp", "http://29.20.130.39:31001/injury/rule/DamageRulePage/DamageRulePage", weight="OTHER ACTION")
        # G.add_edge("http://29.20.130.39:31001/injury/rule/DamageRulePage/DamageRulePage", "http://sso-sit.group.cpic.com/login", weight="OTHER ACTION")
        # G.add_edge("http://sso-sit.group.cpic.com/login", "http://29.20.130.39:31001/injury/welcome", weight="OTHER ACTION")
        # G.add_edge("http://29.20.130.39:31001/injury/welcome", "http://29.20.130.39:31001/injury/toolbox/operation", weight="OTHER ACTION")
        # G.add_edge("http://sso-sit.group.cpic.com/login", "http://29.20.130.39:31001/?SSO_loginName=amlhbmdzdXlp", weight="OTHER ACTION")
        # G.add_edge("http://29.20.130.39:31001/injury/welcome", "http://29.20.130.39:31001/injury/rule/DamageRulePage/DamageRulePage", weight="OTHER ACTION")

        pos = nx.circular_layout(G)

        # 定义边颜色
        node_colors = []
        for node in G.nodes():
            edges = G.out_edges(node, data=True)
            color = 'red'  # 初始颜色
            for _, _, data in edges:
                if data['weight'] == 'STORES ACTION':
                    color = 'blue'
            node_colors.append(color)

        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors)

        # 存储边信息
        stores_action_edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] == "STORES ACTION"]
        url_node_edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] not in ("STORES ACTION")]

        # 画边
        nx.draw_networkx_edges(G, pos, edgelist=stores_action_edges, edge_color='red')
        nx.draw_networkx_edges(G, pos, edgelist=url_node_edges, edge_color='blue')

        # 添加边的标识
        edge_labels = {edge: G[edge[0]][edge[1]]['weight'] for edge in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Role Group: User", size=15)
        plt.axis('off')
        plt.show()


Graph = FSMGraph()

if __name__ == "__main__":
    ori_log_path = r"./source/console.log"
    burp_path = r"./source/result2_29.txt"
    log_path = r"./source/filtered_data.txt"
    filter_clicks_and_write_to_new_file(ori_log_path, log_path)
    config_init()
    GFNA.getFlow(0, "jiangsuyi", burp_path, log_path)
    Graph.load_graph()
    a = 1
