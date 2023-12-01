'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-30 19:03:32
LastEditTime: 2023-12-01 16:50:45
LastEditors: Suez_kip
Description: 
'''
import copy

class HTMLResponse:
    def __init__(self) -> None:
        self.status = -1
        self.response_body = ""

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

class HTMLRequestAnalyzer:
    def __init__(self) -> None:
        self.private_request = HTMLRequest()
        self.example_str = r"D:\Suez_kip\研究生毕设\Code\Tools\RequestsAnalyser\HTMLRequestAnalyzer\PostRequest.txt"

    def getHTMLRequestLines(self, raw_data_path):
        file_path = ""
        tempListPoint = {"name": None, "value": None}
        if raw_data_path == "":
            file_path = self.example_str
        else:
            file_path = raw_data_path
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for index in range(0, len(lines)):
                line = lines[index]
                print(line.strip())  # strip() 用于移除行尾的换行符
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
                        print(temp_list)
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
