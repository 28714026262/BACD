'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-23 20:26:59
LastEditTime: 2024-01-30 14:42:50
LastEditors: Suez_kip
Description: 
'''
import sys
import os
import copy
from WebFlow import GFNA,FlowNode,GWF
from Tools.RequestsAnalyser.HTMLRequestAnalyzer.HTMLRequestAnalyzer import *
from Tools.configloader import *

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
        self.key_num_code = _key_num
        self.Role = _role_name
        self.URL = _url
        self.URL_list = copy.deepcopy(_url_list)
        self.URL_param = copy.deepcopy(_url_param)
        self.WebSourceCodePath = _web_source_code_path

    # function will both recieve the normal action and the connection

class FSM:
    def __init__(self) -> None:
        self.NodeSet = {}
        self.node_last_num = -1
        self.Action = {}
        self.Connection = {}
        self.action_last_num = -1
        self.Role = ""

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

GFSM = FSM()

if __name__ == "__main__":
    config_init()
    burp_path = r"D:\Suez_kip\研究生毕设\Data\jiangsuyi\recorder-jiangsuyi.txt"
    log_path = r"D:\Suez_kip\研究生毕设\Data\jiangsuyi\console-jiangsuyi.log"
    GFNA.getFlow(0, "jiangsuyi", burp_path, log_path)
    a = 1