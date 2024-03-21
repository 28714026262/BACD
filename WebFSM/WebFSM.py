'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-23 20:26:59
LastEditTime: 2024-03-21 17:12:07
LastEditors: Suez_kip
Description: 
'''
import sys
import os
import copy
from WebFlow import GFNA,FlowNode,GWF,FlowSet
from Tools.RequestsAnalyser.HTMLRequestAnalyzer.HTMLRequestAnalyzer import *
from Tools.configloader import *
from Tools.Enumeration import *
import networkx as nx

class RequestWithResponse:
    def __init__(self) -> None:
        self.URL = ""
        self.method = ""
        self.status = ""
        self.header = {}
        self.params_get = {}
        self.params_post = {}
        self.param_body = ""
        self.cookies = {}
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
        self.cookies = copy.deepcopy(flow_node.cookies)
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
        self.cookies = copy.deepcopy(new_Req_Resp.cookies)
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
        self.isAction = 1 # 1 is normal Action, and 2 is Connection
        self.key_num_action = -1
        self.role = ""
        self.src_node_key_num = -1
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
        self.src_node_key_num = newAction.src_node_key_num
        self.req_list = copy.deepcopy(newAction.req_list)

    def action_type_speculate(self):
        # condition1
        self.Type = FSM_ACTION_TYPE_ADD
        # condition2
        self.Type = FSM_ACTION_TYPE_DELETE
        # condition3
        self.Type = FSM_ACTION_TYPE_EDIT
        # condition4
        self.Type = FSM_ACTION_TYPE_READ

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
        if self.src_node_key_num != anotherAction.src_node_key_num:
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
        self.isAction = 2 # 1 is normal Action, and 2 is Connection
        self.dest_node_key_num = -1

    def deepcopy(self, newConnection):
        self.isAction = newConnection.isAction
        self.key_num_action = newConnection.key_num_action
        self.role = copy.deepcopy(newConnection.role)
        self.src_node_key_num = newConnection.src_node_key_num
        self.req_list = copy.deepcopy(newConnection.req_list)
        self.dest_node_key_num = newConnection.src_node_key_num

class Node:
    def __init__(self) -> None:
        self.key_num_code = -1
        self.Role = ""

        self.URL = ""
        self.URL_list = []
        self.URL_param = {}
        self.WebSourceCodePath = ""
        self.action_map_from_self_node = {}
        self.connection_map_from_self_node = {}
        
    def set(self,
            _key_num,
            _role_name,
            _url,
            _url_list,
            _url_param,
            _web_source_code_path) -> None:
        # function will both recieve the normal action and the connection
        self.key_num_code = _key_num
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

class FSM:
    def __init__(self) -> None:
        self.NodeSet = {}
        self.node_last_num = -1
        self.Action = {}
        self.Connection = {}
        self.action_last_num = -1
        self.Role = ""
        self.Role_key_num = -1

        # use networkX
        self.NxContainer = nx.Graph()

    # OLD GAP
    def LoadWebFlowSet(self):
        Main_Data_Set = GFNA.g_flow_role_group_container.flowset
        for flow in Main_Data_Set.FlowsetContainer:
            last_single_node = -1
            for single_node in flow.flow_list_with_gap:
                current_node_key_node = -1
                route_list, url_param = GWF.get_URL_Route(single_node)
                current_node_key_node = self.get_node_by_route_list(route_list)
                if current_node_key_node == -1:
                    localNode = Node()
                    localNode.set(
                        _key_num = self.node_last_num + 1,
                        _role_name = "",
                        _url = single_node,
                        _url_list = route_list,
                        _url_param = url_param,
                        _web_source_code_path = ""
                    )
                    self.node_last_num = self.node_last_num + 1
                    self.NodeSet[str(self.node_last_num)] = localNode
                    current_node_key_node = self.node_last_num
                
                first_flag = True
                for req_seq in flow.flow_list_with_gap[single_node]:
                    if first_flag:
                        first_flag = False
                        if req_seq[2] == 2:
                            self.getAction([last_single_node, current_node_key_node], flow.flow_list[req_seq[0], req_seq[1]])
                        else:
                            self.getAction(current_node_key_node, flow.flow_list[req_seq[0], req_seq[1]])
                    else:
                        self.getAction(current_node_key_node, flow.flow_list[req_seq[0], req_seq[1]])
                last_single_node = current_node_key_node

    # NEW GAP
    def LoadWebFlowSet(self, console_analyze_list, flow_with_gap):
        source_node_key_num = -1
        action_iter = 0
        for console_event_iter in range(console_analyze_list):
            NodeChanged = True
            TabChanged = True
            ClickAction = True
            InputAction = True

            if console_analyze_list[console_event_iter] is TabChanged:# 遇到节点切换
                source_node_key_num = self.haveSameNode(console_analyze_list[console_event_iter].url)
                continue
            if console_analyze_list[console_event_iter] is ClickAction or console_analyze_list[console_event_iter] is InputAction: # 遇到用户点击行为
                if console_analyze_list[console_event_iter + 1] is NodeChanged:
                    is_connection_action = True
                    dest_node_key_num = self.haveSameNode(console_analyze_list[console_event_iter + 1].url)
                    if dest_node_key_num == -1:
                        new_node = Node()
                        # node param fill
                        self.NxContainer.add_node(self.node_last_num)
                        self.node_last_num += 1
                        dest_node_key_num = self.node_last_num
                    self.getAction([source_node_key_num, dest_node_key_num], flow_with_gap[action_iter])
                    source_node_key_num = dest_node_key_num
                else:
                    self.getAction(source_node_key_num, flow_with_gap[action_iter])
            action_iter += 1

    def getAction(self, key_num, req_list):
        if isinstance(key_num, list):
            temp_action = Connection()
            temp_action.isAction = 2 # 1 is normal Action, and 2 is Connection
            self.action_last_num = self.action_last_num + 1
            temp_action.key_num_action = self.action_last_num
            temp_action.role = self.Role
            temp_action.src_node_key_num = key_num[0]
            temp_action.dest_node_key_num = key_num[1]
            self.NodeSet[key_num].connection_map_from_self_node.add(self.action_last_num)
        else:
            temp_action = Action()
            temp_action.isAction = 1 # 1 is normal Action, and 2 is Connection
            self.action_last_num = self.action_last_num + 1
            temp_action.key_num_action = self.action_last_num
            temp_action.role = self.Role
            temp_action.src_node_key_num = key_num
            self.NodeSet[key_num].action_map_from_self_node.add(self.action_last_num)
        
        for req in req_list:
            r_r_container = RequestWithResponse()
            r_r_container.setFromFlowNode(self.NodeSet[key_num].URL, req)
            temp_action.add_Res_and_Resp(r_r_container)

    def get_node_by_route_list(self, url_list) -> int:
        # for node_key_num in self.NodeSet:
        #     if url == self.NodeSet[node_key_num].URL:
        #         return node_key_num
        # return -1
        for node_key_num in self.NodeSet:
            flag, domian_name_useless = GWF.is_Same_URL_Route_by_list(url_list, self.NodeSet[node_key_num].URL_list)
            if flag:
                return node_key_num
        return -1

    def haveSameNode(self):
        pass

class RoleContainer:
    def __init__(self) -> None:
        pass

GFSM = FSM()

if __name__ == "__main__":
    config_init()
    burp_path = r"D:\Suez_kip\研究生毕设\Data\jiangsuyi\recorder-jiangsuyi.txt"
    log_path = r"D:\Suez_kip\研究生毕设\Data\jiangsuyi\console-jiangsuyi.log"
    GFNA.getFlow(0, "jiangsuyi", burp_path, log_path)
    a = 1
