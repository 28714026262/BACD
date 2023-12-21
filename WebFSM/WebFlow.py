'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-24 10:12:07
LastEditTime: 2023-12-21 13:17:38
LastEditors: Suez_kip
Description: 
'''

import os
import sys
sys.path.append(os.getcwd())
import json
import urllib
import copy
import codecs

from Tools.logger import get_logger
from urllib.parse import urlparse
from Tools.RequestsAnalyser.HTMLRequestAnalyzer.HTMLRequestAnalyzer import *
from Tools.DynamicDecoding import *

logger = get_logger(name = os.path.basename(__file__))
global encoding
encoding = "utf-8"

class FlowNode:
    def __init__(self) -> None:
        self.method = ""
        self.url = ""
        self.origin_url = ""
        # self.mimetype = ""
        self.status = ""
        self.header = {}
        self.params_get = {}
        self.params_post = {}
        # self.cookies = {}
        self.response = None
        self.response_text = ""
        
        self.content_type = ""

        self.param_body = ""

    def clear(self):
        self.method = ""
        self.url = ""
        self.origin_url = ""
        # self.mimetype = ""
        self.status = ""
        self.header = {}
        self.params_get = {}
        self.params_post = {}
        # self.cookies = {}
        self.response = None
        self.response_text = ""
        
        self.content_type = ""

        self.param_body = ""
        self.user_action_seq = 0

    def analyze_url_and_get_get_param(self):
        if self.method.lower() == 'get':
            url_list = self.url.split('?')
            if len(url_list) == 2:
                self.origin_url = self.url
                self.url = url_list[0]
                self.params_get = json.dumps(self.extract_param(url_list[1],'application/x-www-form-urlencoded'))

    def extract_param(self, param:str, content_type:str):
        param_dict = {}
        if 'application/x-www-form-urlencoded' in content_type.lower():
            k_v_param = param.strip().split('&')
            #logger.info(encoding)
            for k_v in k_v_param:
                k = urllib.parse.unquote(k_v.split('=', 1)[0],encoding=encoding)
                #由于部分url解码之后由于编码方式原因乱码导致最终错误，因此这里加一次判断机制
                #如果解码出非法字符证明编码不是默认的utf-8，然后尝试使用gbk编码
                if k != '':
                    if len(k_v.split('=', 1)) == 2:

                        v = urllib.parse.unquote(k_v.split('=', 1)[1],encoding=encoding)
                    else:
                        v = ''
                    if v.startswith('{'):#增加对data={XXX:XXX,XXX:xxx}的支持，做法是直接剔除data变为字典
                        try:
                            tmp_dict = json.loads(v)
                        except Exception as e:
                            logger.warning("请求包json解析错误: %s", e.args[0])
                            logger.warning(v)
                        param_dict.update(tmp_dict)
                    else:
                        param_dict[k] = v
        elif 'application/json' in content_type.lower():
            try:
                param_dict = json.loads(param)
            except Exception as e:
                logger.warning("请求包json解析错误: %s", e.args[0])
                logger.warning(param)
            if len(param_dict) == 0 and len(param) > 0:
                return param
        elif 'multipart/form-data' in content_type.lower():
            boundary = ''
            content_type_list = content_type.split("; ")
            for k_v in content_type_list:
                if 'boundary' in k_v:
                    boundary = k_v.split("=",1)[1].strip()
            if boundary:
                try:
                    param_dict = self.convert_multipart_to_dict(param,boundary)
                except Exception as e:
                    logger.warning("请求包form-data解析错误: ", e.args[0])
                    logger.warning(param)
            else:
                logger.warning("multipart/form-data格式错误，按照字符串解析")
                if len(param) > 0 :
                    return param
            if len(param_dict) == 0 and len(param) > 0:
                return param
        elif len(param) > 0 :#有可能发送的是一段字符串，这种情况直接返回,比如'text/xml'
            return param
        return param_dict

    def convert_multipart_to_dict(self, multipart:str,boundary:str) -> dict:
        """将multipart类型的数据转换为字典存储，发送时再编码回multipart"""
        return_dict = {}
        multipart = multipart.replace("\r", "")
        split_multipart = multipart.split("--"+boundary)
        if split_multipart[-1] != '--\n':
            return return_dict
        split_multipart = split_multipart[1:-1]
        for data in split_multipart:
            data = data.strip()
            k_v = data.split("\n\n")
            if len(k_v) == 2:
                v = k_v[1]
                k = k_v[0].split("; ",1)[1].split("=",1)[1]
                k = k.strip("\"")
                return_dict[k] = v
        return return_dict

    def cookie_send_to_dict(self, cookies) -> dict:
        """目前该方法弃用"""
        cookies_dict = {}
        cookies = cookies.strip().split(';')
        for cookie in cookies:
            k = cookie.split('=', 1)[0].strip()
            if k != '':
                if len(cookie.split('=', 1)) == 2:
                    v = cookie.split('=', 1)[1].strip()
                else:
                    v = ''
                cookies_dict[k] = v
        self.cookies = cookies_dict
        return cookies_dict

    def deep_copy(self, node):
        self.method = copy.deepcopy(node.method)
        self.url = node.url
        self.origin_url = node.origin_url
        # self.mimetype = ""
        self.status = node.status
        self.header = copy.deepcopy(node.header)
        self.params_get = copy.deepcopy(node.params_get)
        self.params_post = copy.deepcopy(node.params_post)
        # self.cookies = {}
        self.response = node.response
        self.response_text = node.response_text
        
        self.content_type = node.content_type

        self.param_body = node.param_body
        self.user_action_seq = node.user_action_seq

    def is_same_flow_node(self, node):
        is_same_flag = True
        if self.method != node.method or self.url != node.url:
            is_same_flag = False
        # self.mimetype = ""
        if self.header != node.header or self.user_action_seq != node.user_action_seq: # or self.status != node.status:
            is_same_flag = False

        if self.method.lower() == "get":
            if self.params_get != node.params_get:
                is_same_flag = False
        elif self.method.lower() == "post":
            if self.params_post != node.params_post:
                is_same_flag = False
        return is_same_flag

    def is_action(self):
        pass

    def is_connection(self):
        pass

    def get_whole_dynamic_page(self):
        pass

class Flow:
    def __init__(self) -> None:
        self.flow_list = []
        self.domain_url = ""
        self.url_list = []
        # if CONFIG_DICT["SELF_GET_HTML_FLAG"]:
        #     self.domain_url = ""
        # else:
        #     self.domain_url = CONFIG_DICT["det_domain_name"]

    def append_new_flow_node(self, flow_node: FlowNode):
        flag = self.flow_filter(flow_node)
        # print(flag)
        if flag:
            new_flow_node = FlowNode()
            new_flow_node.deep_copy(flow_node)
            if new_flow_node.content_type != "":
                new_flow_node.method = "POST"
                new_flow_node.params_get = {}
            self.flow_list.append(new_flow_node)

    def flow_filter(self, flow_node: FlowNode) -> bool:
        return_falg = False
        if self.is_useful_req(flow_node.url, flow_node.method, flow_node.params_get) and self.is_useful_url(flow_node.url):
            return_falg = True
        if len(self.flow_list) != 0 and self.flow_list[-1].is_same_flow_node(flow_node):
            return_falg = False
        return return_falg

    def is_useful_url(self, url:str):
        """去除一些静态资源，返回是否是静态资源"""
        if url.split(".")[-1].lower() in (
                            ("bmp", "bz2", "css", "eot", "flv", "gif",
                            "ico", "jpeg", "jpg", "png","js", "less",
                            "rtf", "swf","wav", "woff", "woff2","xml")):
            return False

        # 检测是否是检测目标网站系统
        if self.domain_url != "" and self.domain_url not in url:
            return False
        if "/record/saveV" in url:
            return False
        return True

    def is_useful_req(self, url,method:str,params_get) -> bool:
        """去除一些没有参数的get请求，避免请求对流程无用的数据包"""
        path = urlparse(url).path
        if method.lower() == "get":
            if params_get != json.dumps({}):
                return True
            if path != '' and path != '/':
                return True
            return False
        return True

    def get_domain_url(self):
        url_dict = {}
        new_domain_url = ""
        for url_str in self.url_list:
            if "?" in url_str:
                end_position = url_str.index("?")
            if "http" in url_str:
                start_position = url_str.index("http") + 7
                if "https" in url_str:
                    start_position = start_position + 1

            url_str = url_str[start_position: end_position]
            if "/" in url_str:
                end_position = url_str.index("/")
            url_str = url_str[0: end_position]
            if not url_str in url_dict:
                url_dict[url_str] = 1
            else:
                url_dict[url_str] = url_dict[url_str] + 1
        
        first_flag = True
        max_url_time = -1
        max_url = ""
        for url, url_appear_time in url_dict.items():
            if max_url_time < url_appear_time or first_flag:
                max_url_time = url_appear_time
                max_url = url
                first_flag = False
        new_domain_url = max_url
        self.domain_url = new_domain_url
        return new_domain_url

    def show_flow_list(self):
        for flow_node in self.flow_list:
            flow_node.show()

    def save_to_sqlite(self):        
        pass

    def page_analyzer(self):
        pass

class FlowSet:
    def __init__(self) -> None:
        self.Flowset = {}
    
    def flowSetAppend(self, NewFlow: Flow):
        self.Flowset.add(NewFlow)

    def getSameFlowNode(self, sourceFlowNode: FlowNode):
        result = -1
        for targetFlows in self.Flowset:
            for index, targetNode in targetFlows.flow_list:
                compare_result = targetNode.is_same_flow_node(sourceFlowNode)
                if compare_result:
                    result = index
        return result

class FlowRoleGroup:
    def __init__(self) -> None:
        self.flowset = FlowSet()
        self.role_name = ""

class FlowAnalysis:
    def __init__(self) -> None:
        pass

class Global_Flow_Node_Analyser:
    def __init__(self) -> None:
        self.g_flow_node_container = FlowNode()
        self.g_flow_container = Flow()
        self.g_flow_set_container = FlowSet()
        self.g_flow_role_group_container = FlowRoleGroup()
        self.g_flow_analyser = FlowAnalysis()
        self.flow_node_stop_flag = True
        self.HRA = HTMLRequestAnalyzer()
        self.HRA_Init_Flag = False
        self.G_FLOW_LOADED_FLAG = False

    # Request类目前适配Playwright的，需要修改；
    # def getDataFromTrafficwithRequests(self, response: requests.Response):
    #     tempRequest = response.request
    #     url_str = tempRequest.url
    #     if url_str.find("?") == -1:
    #         url = url_str
    #     else: 
    #         url = url_str[0:url_str.find("?")]
    #     if tempRequest.post_data:
    #         logger.debug(tempRequest.post_data)
    #     if self.g_flow_container.is_useful_url(url):
    #         self.g_flow_node_container.clear()
    #         self.flow_node_stop_flag = True
    #         self.g_flow_node_container.method = tempRequest.method
    #         self.g_flow_node_container.url = tempRequest.url
    #         # self.g_flow_node_container.mimetype = ""
    #         for header_item in tempRequest.headers_array():
    #             self.g_flow_node_container.header[header_item['name']] = header_item['value']
    #         self.g_flow_node_container.analyze_url_and_get_get_param()
    #         self.g_flow_node_container.param_body = tempRequest.post_data
    #         self.g_flow_node_container.params_post = {}
    #         if self.g_flow_node_container.method.lower() == "post":
    #             if "Content-Type" in self.g_flow_node_container.header:
    #                 content_type_str = self.g_flow_node_container.header["Content-Type"]
    #                 # self.g_flow_node_container.content_type = content_type_str[0: content_type_str.find(";")]
    #                 self.g_flow_node_container.content_type = content_type_str
    #             if self.g_flow_node_container.param_body:
    #                 self.g_flow_node_container.params_post = self.g_flow_node_container.extract_param(self.g_flow_node_container.param_body, self.g_flow_node_container.content_type)
    #         else:
    #             self.g_flow_node_container.content_type = ""
    #         # self.g_flow_node_container.cookies = {}  
    #         self.g_flow_node_container.response = tempRequest.response()
    #         if self.g_flow_node_container.response:
    #             self.g_flow_node_container.status = self.g_flow_node_container.response.status
    #     # if self.g_flow_node_container.response.status == 200:
    #     #     try:
    #     #         self.g_flow_node_container.response_text = self.g_flow_node_container.response.text()
    #     #     except Exception as e:
    #     #         self.g_flow_node_container.show()
    #     # else:
    #     #     self.g_flow_node_container.response_text = ""        
    #     self.g_flow_container.append_new_flow_node(self.g_flow_node_container)

    def getDataFromTraffic(self):
        if not self.HRA_Init_Flag:
            logger.debug("No HRA Init!")
            return
        if self.HRA.private_request.method_flag != -1:
            tempRequest = self.HRA.private_request
            url_str = tempRequest.url
            if url_str.find("?") == -1:
                url = url_str
            else: 
                url = url_str[0:url_str.find("?")]
            if tempRequest.post_data:
                logger.debug(tempRequest.post_data)
            if self.g_flow_container.is_useful_url(url):
                self.g_flow_node_container.clear()
                self.flow_node_stop_flag = True
                self.g_flow_node_container.method = tempRequest.method
                self.g_flow_node_container.url = tempRequest.url
                # self.g_flow_node_container.mimetype = ""
                for header_item in tempRequest.headers_array():
                    self.g_flow_node_container.header[header_item['name']] = header_item['value']
                self.g_flow_node_container.analyze_url_and_get_get_param()
                self.g_flow_node_container.param_body = tempRequest.post_data
                self.g_flow_node_container.params_post = {}
                if self.g_flow_node_container.method.lower() == "post":
                    if "Content-Type" in self.g_flow_node_container.header:
                        content_type_str = self.g_flow_node_container.header["Content-Type"]
                        # self.g_flow_node_container.content_type = content_type_str[0: content_type_str.find(";")]
                        self.g_flow_node_container.content_type = content_type_str
                    if self.g_flow_node_container.param_body:
                        self.g_flow_node_container.params_post = self.g_flow_node_container.extract_param(self.g_flow_node_container.param_body, self.g_flow_node_container.content_type)
                else:
                    self.g_flow_node_container.content_type = ""
                # self.g_flow_node_container.cookies = {}  
            if tempRequest.response.status != -1:
                self.g_flow_node_container.response = tempRequest.response
                self.g_flow_node_container.status = self.g_flow_node_container.response.status

    def getHRAInPath(self, req_path, resp_path):
        self.HRA.getRequestInPath(req_path)
        self.HRA.getResponseInPath(resp_path)
        self.HRA_Init_Flag = True

    def getHRAInStr(self, req_str, resp_str):
        self.HRA.getRequestInStr(req_str)
        self.HRA.getResponseInStr(resp_str)
        self.HRA_Init_Flag = True
        
    def getHRAInLines(self, req_lines, resp_lines, resp_exist_flag):
        self.HRA.getHTMLRequestLines(req_lines)
        if resp_exist_flag:
            self.HRA.getHTMLResponseLines(resp_lines)
        self.HRA_Init_Flag = True

    def flowAppend(self):
        self.g_flow_container.append_new_flow_node(self.g_flow_node_container)
        self.HRA_Init_Flag = False

    def BurpResultSuiterToFlow(self, path):
        whole_HTML_message = {"req_list": [], "resp_list": []}
        count = 0
        request_data_in_flag = False
        response_data_in_flag = False
        response_exist_flag = True
        first_response_line_flag = False
        with codecs.open(path, 'rb') as file:
            lines = []
            for line in file:
                lines.append(handleEncoding(line))
            for line in lines:
                if "====" in line:
                    count = (count + 1) % 4
                    if count == 3:
                        request_data_in_flag = False
                if count == 2:
                    # request attach
                    if request_data_in_flag:
                        whole_HTML_message["req_list"].append(line)
                    else:
                        request_data_in_flag = True
                if count == 3 and response_exist_flag:
                    # response attach
                    if response_data_in_flag:
                        if "HTTP" not in line and first_response_line_flag:
                            response_exist_flag = False
                            count = (count + 1) % 4
                        first_response_line_flag = False
                        whole_HTML_message["resp_list"].append(line)
                    else:
                        response_data_in_flag = True
                        first_response_line_flag = True
                if count == 0 and whole_HTML_message["req_list"] != []:
                        self.getHRAInLines(whole_HTML_message["req_list"], whole_HTML_message["resp_list"], response_exist_flag)
                        self.getDataFromTraffic()
                        whole_HTML_message["req_list"] = []
                        whole_HTML_message["resp_list"] = []
                        response_data_in_flag = False
                        response_exist_flag = True
                        if self.g_flow_node_container.method:
                            self.flowAppend()
                        self.HRA.clear()
                        self.g_flow_node_container.clear()
        self.G_FLOW_LOADED_FLAG = True
        self.get_url_list()

    def UnrelatedTrafficFromURL(self):
        host_url_str = ""
        host_url_sub_str = ""
        host_flag = False
        if self.g_flow_container.flow_list:
            for list_node in self.g_flow_container.flow_list:
                if "Host" in list_node.header:
                    host_url_str = list_node.header["Host"]
                    host_flag = True
                elif "host" in list_node.header:
                    host_url_str = list_node.header["host"]
                    host_flag = True

                host_url_sub_str = list_node.url
                if host_flag:
                    # filter on host_url
                    self.url_filter(host_url_str)
                else:
                    # filter on url
                    self.url_filter(host_url_sub_str)
        pass
    
    def get_url_list(self):
        if not self.G_FLOW_LOADED_FLAG:
            return
        host = ""
        temp_url = ""
        for node_container in self.g_flow_container.flow_list:
            if "Host" in node_container.header:
                host = node_container.header["Host"]
            elif "host" in node_container.header:
                host = node_container.header["host"]
            if host:
                if node_container.origin_url:
                    temp_url = host + node_container.origin_url
                else:
                    temp_url = host + node_container.url
            else:
                if node_container.origin_url:
                    temp_url = node_container.origin_url
                else:
                    temp_url = node_container.url
            if temp_url not in self.g_flow_container.url_list:
                logger.debug("temp_url : " + temp_url)
                self.g_flow_container.url_list.append(temp_url)

    def url_filter(self, str):
        pass

if __name__ == "__main__":
    GFNA = Global_Flow_Node_Analyser()
    GFNA.BurpResultSuiterToFlow(r"D:\Suez_kip\研究生毕设\Code\Test\Source\Flow.txt")
    a = 1