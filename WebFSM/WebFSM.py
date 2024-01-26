'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-23 20:26:59
LastEditTime: 2024-01-26 15:07:27
LastEditors: Suez_kip
Description: 
'''
import sys
import os
import copy
from WebFlow import GFNA, Global_Flow_Node_Analyser,FlowNode
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
        self.WebSourceCodePath = ""
        self.action_map_from_self_node = {}
        self.connection_map_from_self_node = {}
        
    def set(self,
            _key_num,
            _role_name,
            _url,
            _web_source_code_path) -> None:
        self.key_num_code = _key_num
        self.Role = _role_name
        self.URL = _url
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

    def LoadWebFlow(self):
        Main_Data_Set = GFNA.g_flow_role_group_container.flowset
        for flow in Main_Data_Set:
            last_single_node = -1
            for single_node in flow.flow_list_with_gap:
                localNode = Node()
                localNode.set(
                    _key_num = self.node_last_num + 1,
                    _role_name = "",
                    _url = single_node,
                    _web_source_code_path = ""
                )
                self.node_last_num = self.node_last_num + 1
                self.NodeSet[str(self.node_last_num + 1)] = localNode
                
                first_flag = True
                for req_seq in flow.flow_list_with_gap[single_node]:
                    if first_flag:
                        first_flag = False
                        if req_seq[2] == 2:
                            self.getAction([last_single_node, localNode.key_num_code], flow.flow_list[req_seq[0], req_seq[1]])
                        else:
                            self.getAction(localNode.key_num_code, flow.flow_list[req_seq[0], req_seq[1]])
                    else:
                        self.getAction(localNode.key_num_code, flow.flow_list[req_seq[0], req_seq[1]])
                last_single_node = self.node_last_num + 1

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

    def get_node_by_name(self, url) -> int:
        for node_key_num in self.NodeSet:
            if url == self.NodeSet[node_key_num].URL:
                return node_key_num
        return -1

GFSM = FSM()

if __name__ == "__main__":
    config_init()
    burp_path = r"D:\Suez_kip\研究生毕设\Data\jiangsuyi\recorder-jiangsuyi.txt"
    log_path = r"D:\Suez_kip\研究生毕设\Data\jiangsuyi\console-jiangsuyi.log"
    GFNA.getFlow(0, "jiangsuyi", burp_path, log_path)
    a = 1