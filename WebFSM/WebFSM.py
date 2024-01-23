import sys
import os
import copy
from WebFlow import GFNA, Global_Flow_Node_Analyser

class RequestWithResponse:
    def __init__(self) -> None:
        self.URL = ""

        self.request_raw_data_path = ""
        self.request_raw_data = ""
        self.request_header_map = {}
        self.request_body = ""
        self.param_in_URL_map = {}
        self.param_in_body_map = {}

        self.response_raw_data_path = ""
        self.response_raw_data = ""
        self.response_status_code = 0
    
    def deepcopy(self, new_Req_Resp):
        self.URL = copy.deepcopy(new_Req_Resp.URL)
        self.request_raw_data_path = copy.deepcopy(new_Req_Resp.request_raw_data_path)
        self.request_raw_data = copy.deepcopy(new_Req_Resp.request_raw_data)
        self.request_header_map = copy.deepcopy(new_Req_Resp.request_header_map)
        self.request_body = copy.deepcopy(new_Req_Resp.request_body)
        self.param_in_URL_map = copy.deepcopy(new_Req_Resp.param_in_URL_map)
        self.param_in_body_map = copy.deepcopy(new_Req_Resp.param_in_body_map)

        self.response_raw_data_path = copy.deepcopy(new_Req_Resp.response_raw_data_path)
        self.response_raw_data = copy.deepcopy(new_Req_Resp.response_raw_data)
        self.response_status_code = new_Req_Resp.response_status_code

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
        for req in newAction.req_list:
            self.req_list.append

class Connection(Action):
    def __init__(self) -> None:
        super(Connection, self).__init__()
        self.isAction = 2 # 1 is normal Action, and 2 is Connection
        self.dest_node_key_num = -1

    def deepcopy(self, newConnection):
        pass

class Node:
    def __init__(self) -> None:
        self.key_num_code = -1
        self.Role = ""

        self.URL = ""
        self.WebSourceCodePath = ""
        self.action_map_from_self_node = {}
        self.connection_map_from_self_node = {}

    # function will both recieve the normal action and the connection
    def getNewAction(self, newAction: Action): 
        if newAction.isAction == 1:
            if newAction.key_num_action not in self.action_map_from_self_node:
                self.connection_map_from_self_node[newAction.key_num_action] = 
        elif newAction.isAction == 2:
            pass

class FSM:
    def __init__(self) -> None:
        self.NodeSet = {}
        self.Action = {}
        self.Connection = {}

    def LoadWebFlow(self, localGFNA: Global_Flow_Node_Analyser):
        Main_Data_Set = localGFNA.g_flow_set_container
        