'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-30 19:03:32
LastEditTime: 2023-12-05 17:09:04
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
        self.headers_list = []
    
    def headers_array(self):
        return self.headers_list
    
    def clear(self):
        self.status = -1
        self.response_body = ""
        self.status_str = ""
        self.protocol = ""
        self.headers_list = []

class HTMLRequest:
    def __init__(self) -> None:
        self.url = ""
        self.post_data = ""
        self.method = ""
        self.method_flag = -1 # 0为GET，1为POST
        self.protocol = ""
        self.headers_list = []
        self.response = HTMLResponse()

    def headers_array(self):
        return self.headers_list

    def clear(self):
        self.url = ""
        self.post_data = ""
        self.method = ""
        self.method_flag = -1 # 0为GET，1为POST
        self.protocol = ""
        self.headers_list = []
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
                requestType_and_URL_and_protocol = line.split(" ", 2)
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
                    tempListPoint["name"] = temp_list[0]
                    if "content" in temp_list[0] or "Content" in temp_list[0] or "CONTENT" in temp_list[0]:
                        content_flag = True
                    tempListPoint["value"] = temp_list[1]
                    new_list_node = copy.deepcopy(tempListPoint)
                    tempListPoint = {"name": None, "value": None}
                    self.private_request.response.headers_list.append(new_list_node)
                else:
                    content_start_flag = True

    def getHTMLRequestLines(self, lines):
        tempListPoint = {"name": None, "value": None}
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
            elif index == len(lines) - 1:
                if self.private_request.method_flag == 0:
                    pass
                elif self.private_request.method_flag == 1:
                    self.private_request.post_data = line
            else:
                if any(c.isalpha() for c in line) or any(c.isdigit() for c in line):
                    temp_list = self.lineToDictPair(line.strip())
                    logger.debug(temp_list)
                    tempListPoint["name"] = temp_list[0]
                    tempListPoint["value"] = temp_list[1]
                    new_list_node = copy.deepcopy(tempListPoint)
                    tempListPoint = {"name": None, "value": None}
                    self.private_request.headers_list.append(new_list_node)
                else:
                    continue

    def lineToDictPair(self, str_line):
        result_list = str_line.split(': ', 1)
        return result_list
