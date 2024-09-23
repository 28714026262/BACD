import copy
import re
import json
example_file_path = r'./source/filtered_data.txt'

import os
import sys
sys.path.append(os.getcwd())
from Tools.logger import get_logger
logger = get_logger(name = os.path.basename(__file__))

TAB_SWITCH_HRG = 1
URL_UPDATED_HRG = 2
#增加两个标识
CLICK_ACTION_HRG = 3
INPUT_ACTION_HRG = 4

#对click element作存储
class click_element_container:
    def __init__(self) -> None:
        self.tagName = ""
        self.id = ""
        self.className = ""
        self.text = ""
        self.path = ""
        self.timestamp = ""

    def clear(self):
        self.tagName = ""
        self.id = ""
        self.className = ""
        self.text = ""
        self.path = ""
        self.timestamp = ""

    def deepcopy(self, new_element):
        if new_element != {}:
            if type(new_element) == dict:
                self.tagName = copy.deepcopy(new_element["tagName"])
                self.id = copy.deepcopy(new_element["id"])
                self.className = copy.deepcopy(new_element["className"])
                self.text = copy.deepcopy(new_element["text"])
                self.path = copy.deepcopy(new_element["path"])
                self.timestamp = copy.deepcopy(new_element["timestamp"])
            else:
                self.tagName = copy.deepcopy(new_element.tagName)
                self.id = copy.deepcopy(new_element.id)
                self.className = copy.deepcopy(new_element.className)
                self.text = copy.deepcopy(new_element.text)
                self.path = copy.deepcopy(new_element.path)
                self.timestamp = copy.deepcopy(new_element.timestamp)

#对input element作存储
class input_element_container:
    def __init__(self) -> None:
        self.type = ""
        self.value = ""
        self.id = ""
        self.className = ""
        self.tagName = ""

    def clear(self):
        self.type = ""
        self.value = ""
        self.id = ""
        self.className = ""
        self.tagName = ""

    def deepcopy(self, new_element):
        if new_element != {}:
            if type(new_element) == dict:
                self.type = new_element["type"]
                self.value = new_element["value"]
                self.id = new_element["id"]
                self.className = new_element["className"]
                self.tagName = new_element["tagName"]
            else:
                self.type = copy.deepcopy(new_element.type)
                self.value = copy.deepcopy(new_element.value)
                self.id = copy.deepcopy(new_element.id)
                self.className = copy.deepcopy(new_element.className)
                self.tagName = copy.deepcopy(new_element.tagName)

class HTTP_request_Gap:
    def __init__(self) -> None:
        self.time = -1
        self.activated_URL = ""
        self.changed_URL = ""
        #增加click input action
        self.click_action = ""
        self.input_action = ""
        self.click_element = click_element_container()
        self.input_element = input_element_container()
        self.gap_type = -1
    
    def clear(self):
        self.time = -1
        self.activated_URL = ""
        self.changed_URL = ""
        #增加click input action
        self.click_action = ""
        self.input_action = ""
        self.click_element.clear()
        self.input_element.clear()
        self.gap_type = -1
    
    def deepcopy(self, new_gap):
        self.time = new_gap.time
        self.activated_URL = copy.deepcopy(new_gap.activated_URL)
        self.changed_URL = copy.deepcopy(new_gap.changed_URL)
        #增加click input action
        self.click_action = copy.deepcopy(new_gap.click_action)
        self.input_action = copy.deepcopy(new_gap.input_action)
        self.click_element.deepcopy(new_gap.click_element)
        self.input_element.deepcopy(new_gap.input_element)
        self.gap_type = new_gap.gap_type

#若检测到为element details，则进行拆分
#1为click elements, 2为input elements
def parse_element_details(type, details_str):
    if type == 1:
        temp_con = click_element_container()
        details_parts = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", details_str)
        for part in details_parts:
            split_part = part.split(':', 1)
            if len(split_part) == 2:
                key, value = split_part
                key = key.strip()
                value = value.strip().strip("'")
                if key == "tagName":
                    temp_con.tagName = value.strip().strip("'")
                elif key == "id":
                    temp_con.id = value.strip().strip("'")
                elif key == "className":
                    temp_con.className = value.strip().strip("'")
                elif key == "text":
                    temp_con.text = value.strip().strip("'")
                elif key == "path":
                    temp_con.path = value.strip().strip("'")
                elif key == "timestamp":
                    temp_con.timestamp = value.strip().strip("'")
            else:
                continue

        return temp_con

    elif type == 2:
        temp_con = input_element_container()
        details_parts = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", details_str)
        for part in details_parts:
            split_part = part.split(':', 1)
            if len(split_part) == 2:
                key, value = split_part
                key = key.strip()
                value = value.strip().strip("'")
                if key == "type":
                    temp_con.type = value.strip().strip("'")
                elif key == "value":
                    temp_con.value = value.strip().strip("'")
                elif key == "id":
                    temp_con.id = value.strip().strip("'")
                elif key == "className":
                    temp_con.className = value.strip().strip("'")
                elif key == "tagName":
                    temp_con.tagName= value.strip().strip("'")
            else:
                continue

        return temp_con

#将line进行拆分，装载进temp_gap_map
#对input和click的element details作分析
def analyze_line(input_str):
    data_dict = {}
    if not input_str.startswith("background"):
        input_str = input_str.strip()
        input_json = json.loads(input_str)
        if "URLChanged" in input_json:
            data_dict["Time"] = input_json["Time"][1:-1]
            data_dict["NodeChanged"] = input_json["URLChanged"][1:-1]
        elif "ActivatedURL" in input_json:
            data_dict["Time"] = input_json["Time"][1:-1]
            data_dict["TabChanged"] = ""
        elif "ClickDetected" in input_json:
            data_dict["Time"] = input_json["Time"][1:-1]
            data_dict["ClickAction"] = input_json["ClickDetected"]
            data_dict["ElementDetails"] = input_json["ElementDetails"]
        elif "InputDetected" in input_json:
            data_dict["Time"] = input_json["Time"][1:-1]
            data_dict["InputAction"] = input_json["InputDetected"]
            data_dict["InputDetails"] = input_json["InputDetails"]
    else:
        pattern = r'(\w+):\s*(?:\{\s*([^\}]*?)\s*\}|\[\s*([^\]]*?)\s*\])\s*'
        matches = re.findall(pattern, input_str, re.DOTALL)
        match_list = []
        for match in matches:
            key = match[0]
            value = match[1] if match[1] else match[2]
            value = value.strip()
            match_list.append((key, value))
        CLICK_DETECTED = False
        INPUT_DETECTED = False
        for match in match_list:
            key, value = match
            if key == "ClickDetected":
                CLICK_DETECTED = True
                data_dict["ClickAction"] = value.strip('{}[]')
            elif key == "InputDetected":
                INPUT_DETECTED = True
                data_dict["InputAction"] = value.strip('{}[]')
            elif key == "ActivatedURL":
                data_dict["TabChanged"] = value.strip('{}[]')
            elif key == "URLChanged":
                data_dict["NodeChanged"] = value.strip('{}[]')
            elif CLICK_DETECTED and key == "ElementDetails":
                CLICK_DETECTED = False
                data_dict[key] = parse_element_details(1, value.strip('{}[]'))
            elif INPUT_DETECTED and key == "InputDetails":
                INPUT_DETECTED = False
                data_dict[key] = parse_element_details(2, value.strip('{}[]'))
            else:
                data_dict[key] = value.strip('{}[]')

    return data_dict

def ChromeExtensionLoader(file_path):
    HTTP_request_Gap_List = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        temp_gap = HTTP_request_Gap()

        # 结构：[标志，名称]；标识中 1 为 ID, 2 为 className；
        last_input_target_id = [-1, ""]

        for line in lines:
            #装载temp_gap_map
            temp_gap_map = analyze_line(line)
            #print(temp_gap_map)
                # 是否需要根据输入覆盖上次输入
            should_cover_Latest_action_according_to_input_target_flag = False

            #属性改TabChanged
            if 'TabChanged' in temp_gap_map:
                temp_gap.clear()
                temp_gap.time = temp_gap_map['Time']
                temp_gap.activated_URL = temp_gap_map['TabChanged']
                temp_gap.gap_type = TAB_SWITCH_HRG
            #属性改NodeChanged
            elif 'NodeChanged' in temp_gap_map:
                temp_gap.clear()
                temp_gap.time = temp_gap_map['Time']
                temp_gap.changed_URL = temp_gap_map['NodeChanged']
                temp_gap.gap_type = URL_UPDATED_HRG
            #增加click判定，属性为ClickAction
            elif 'ClickAction' in temp_gap_map:
                temp_gap.clear()
                temp_gap.time = temp_gap_map['Time']
                #更改参数
                temp_gap.click_action = temp_gap_map['ClickAction']
                temp_gap.click_element = temp_gap_map['ElementDetails']
                temp_gap.gap_type = CLICK_ACTION_HRG
            #增加input判定，属性为InputAction
            elif 'InputAction' in temp_gap_map:
                temp_gap.clear()
                temp_gap.time = temp_gap_map['Time']
                #更改参数
                temp_gap.input_action = temp_gap_map['InputAction']
                temp_gap.input_element = temp_gap_map['InputDetails']
                temp_gap.gap_type = INPUT_ACTION_HRG
                
                # 整合输入动作
                # targetKey = []
                # if "id" in temp_gap.input_element and temp_gap.input_element["id"] != "":
                #     targetKey = [1, temp_gap.input_element["id"]]
                # elif "className" in temp_gap.input_element and temp_gap.input_element["className"] != "":
                #     targetKey = [2, temp_gap.input_element["className"]]
                # else:
                #     logger.error("No ID element been inputed!", temp_gap.input_element)

                # if targetKey != []:
                #     if targetKey[0] == last_input_target_id[0] and targetKey[1] == last_input_target_id[1]:
                #         should_cover_Latest_action_according_to_input_target_flag = True
                #     last_input_target_id[0] = targetKey[0]
                #     last_input_target_id[1] = targetKey[1]

            gap_append = HTTP_request_Gap()
            gap_append.deepcopy(temp_gap)
            # if should_cover_Latest_action_according_to_input_target_flag:
            if False:
                HTTP_request_Gap_List[-1] = gap_append
            else:
                HTTP_request_Gap_List.append(gap_append)
        print("HTTP_request_Gap_List", HTTP_request_Gap_List)
    return HTTP_request_Gap_List

if __name__ == "__main__":
    ChromeExtensionLoader(example_file_path)
