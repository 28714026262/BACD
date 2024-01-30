'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-30 19:03:32
LastEditTime: 2024-01-30 16:49:40
LastEditors: Suez_kip
Description: 
'''
import copy
from Tools.logger import get_logger
import os

logger = get_logger(name = os.path.basename(__file__))
class HTMLResponse:
    def __init__(self) -> None:
        self.status = -1
        self.response_body = ""
        self.status_str = ""
        self.protocol = ""
        self.headers_map = []
        self.content_type = ""
    
    def headers_array(self):
        return self.headers_map

    def deepcopy(self, new_resp):
        self.status = new_resp.status
        self.response_body = copy.deepcopy(new_resp.response_body)        
        self.status_str = copy.deepcopy(new_resp.status_str)
        self.protocol = copy.deepcopy(new_resp.protocol)
        self.headers_map = copy.deepcopy(new_resp.headers_map)
        self.content_type = copy.deepcopy(self.content_type)
    
    def clear(self):
        self.status = -1
        self.response_body = ""
        self.status_str = ""
        self.protocol = ""
        self.headers_map = []
        self.content_type = ""

    def is_same_response(self, input_resp):
        pass

class HTMLRequest:
    def __init__(self) -> None:
        self.url = ""
        self.post_data = ""
        self.method = ""
        self.method_flag = -1 # 0为GET，1为POST
        self.protocol = ""
        self.headers_map = []
        self.response = HTMLResponse()

    def deepcopy(self, new_req) -> None:
        self.url = copy.deepcopy(new_req.url)
        self.post_data = copy.deepcopy(new_req.post_data)
        self.method = copy.deepcopy(new_req.method)
        self.method_flag = new_req.method_flag # 0为GET，1为POST
        self.protocol = copy.deepcopy(new_req.protocol)
        self.headers_map = copy.deepcopy(new_req.headers_map)
        self.response.deepcopy(new_req.response)

    def headers_array(self):
        return self.headers_map

    def clear(self):
        self.url = ""
        self.post_data = ""
        self.method = ""
        self.method_flag = -1 # 0为GET，1为POST
        self.protocol = ""
        self.headers_map = []
        self.response.clear()

class HTMLRequestAnalyzer:
    def __init__(self) -> None:
        self.private_request = HTMLRequest()
        
    def clear(self):
        self.private_request.clear()

    def getRequestInStr(self, raw_data: str):
        if raw_data:
            lines = raw_data.split("\n")
            self.getHTMLRequestLines(lines)
        else:
            logger.debug("Empty raw request data string!")

    def getResponseInStr(self, raw_data: str):
        if raw_data:
            lines = raw_data.split("\n")
            self.getHTMLResponseLines(lines)
        else:
            logger.debug("Empty raw response data string!")

    def getRequestInPath(self, raw_data_path):
        file_path = ""
        file_path = raw_data_path
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.getHTMLRequestLines(lines)

    def getResponseInPath(self, raw_data_path):
        file_path = ""
        file_path = raw_data_path
        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()
            self.getHTMLResponseLines(lines)

    def getHTMLResponseLines(self, lines):
        tempListPoint = {"name": None, "value": None}
        content_flag = False
        content_start_flag = False
        for index in range(0, len(lines)):
            line = lines[index].strip()
            if index == 0:
                requestType_and_URL_and_protocol = line.split(" ")
                if len(requestType_and_URL_and_protocol) > 3:
                    for str in requestType_and_URL_and_protocol[2:]:
                        self.private_request.response.status_str = self.private_request.response.status_str + str + " "
                    self.private_request.response.status_str = self.private_request.response.status_str[:len(self.private_request.response.status_str) - 1]
                if len(requestType_and_URL_and_protocol) == 3:
                    self.private_request.response.status_str = requestType_and_URL_and_protocol[2]

                self.private_request.response.status = requestType_and_URL_and_protocol[1]
                self.private_request.response.protocol = requestType_and_URL_and_protocol[0].upper()
            elif content_start_flag and content_flag:
                if self.private_request.response.response_body:
                    self.private_request.response.response_body = self.private_request.response.response_body + r"\n" + line
                else:
                    self.private_request.response.response_body = line
            else:
                if any(c.isalpha() for c in line) or any(c.isdigit() for c in line):
                    temp_list = self.lineToDictPair(line.strip())
                    logger.debug(temp_list)
                    if len(temp_list) == 1:
                        continue
                    if "content" in temp_list[0] or "Content" in temp_list[0] or "CONTENT" in temp_list[0]:
                        self.private_request.response.content_type = temp_list[1]
                    self.private_request.response.headers_map.append(copy.deepcopy({"name": temp_list[0], "value": temp_list[1]}))
                else:
                    content_start_flag = True

    def getHTMLRequestLines(self, lines):
        tempListPoint = {"name": None, "value": None}
        post_body_flag = False
        first_post_line_flag = True
        for index in range(0, len(lines)):
            line = lines[index]
            if index == 0:
                requestType_and_URL_and_protocol = line.split(" ", 2)
                self.private_request.protocol = requestType_and_URL_and_protocol[2]
                self.private_request.url = requestType_and_URL_and_protocol[1]
                self.private_request.method = requestType_and_URL_and_protocol[0].upper()
                if self.private_request.method == "GET":
                    self.private_request.method_flag = 0
                elif self.private_request.method == "POST":
                    self.private_request.method_flag = 1
            elif (index == len(lines) - 1) or post_body_flag:
                if self.private_request.method_flag == 0:
                    pass
                elif self.private_request.method_flag == 1:
                    if first_post_line_flag:
                        self.private_request.post_data = line
                        first_post_line_flag = False
                    else:
                        self.private_request.post_data += line
            else:
                if any(c.isalpha() for c in line) or any(c.isdigit() for c in line):
                    temp_list = self.lineToDictPair(line.strip())
                    logger.debug(temp_list)
                    tempListPoint["name"] = temp_list[0]
                    if len(temp_list) == 1:
                        tempListPoint["value"] = ""
                    else:
                        tempListPoint["value"] = temp_list[1]
                    new_list_node = copy.deepcopy(tempListPoint)
                    tempListPoint = {"name": None, "value": None}
                    self.private_request.headers_map.append(new_list_node)
                else:
                    post_body_flag = True
                    continue

    def lineToDictPair(self, str_line):
        result_list = str_line.split(': ', 1)
        return result_list
        a = 1