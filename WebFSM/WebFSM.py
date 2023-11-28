import sys
import os

class Node:
    def __init__(self) -> None:
        self.node_key_num = -1
        self.Role = ""

        self.URL = ""
        self.WebSourceCodePath = ""

class Action:
    def __init__(self) -> None:
        self.role = ""
        self.src_node_key_num = -1

        self.URL = ""

        self.request_raw_data_path = ""
        self.request_raw_data = ""
        self.request_header = ""
        self.request_body = ""
        self.param_in_URL_map = {}
        self.param_in_body_map = {}

        self.response_raw_data_path = ""
        self.response_raw_data = ""
        self.response_status_code = 0


class Connection:
    def __init__(self) -> None:
        self.role = ""
        self.node_key_num_edge = [-1, -1]

        self.URL = ""

        self.request_raw_data_path = ""
        self.request_raw_data = ""
        self.request_header = ""
        self.request_body = ""
        self.param_in_URL_map = {}
        self.param_in_body_map = {}

        self.response_raw_data_path = ""
        self.response_raw_data = ""
        self.response_status_code = 0

class FSM:
    def __init__(self) -> None:
        self.NodeSet = {}
        self.Action = {}
        self.Connection = {}

    def Minus(self):
        pass

    def GetChokeliointPoint(self):
        pass
