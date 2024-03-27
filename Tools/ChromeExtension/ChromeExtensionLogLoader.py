import copy
import os
import re
example_file_path = r'C:/Users/User/Downloads/BACD/BACD-main/source/filtered_data.txt'

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
    pattern = r'(\w+):\s*(?:\{\s*([^\}]*?)\s*\}|\[\s*([^\]]*?)\s*\])\s*'
    matches = re.findall(pattern, input_str, re.DOTALL)
    match_list = []
    for match in matches:
        key = match[0]
        value = match[1] if match[1] else match[2]
        value = value.strip()
        match_list.append((key, value))
    data_dict = {}
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
    #print(data_dict)
    return data_dict

def ChromeExtensionLoader(file_path):
    HTTP_request_Gap_List = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        temp_gap = HTTP_request_Gap()
        for line in lines:
            #装载temp_gap_map
            temp_gap_map = analyze_line(line)
            #print(temp_gap_map)
            for key, value in temp_gap_map.items():
                #属性改TabChanged
                if key == 'TabChanged':
                    temp_gap.clear()
                    temp_gap.time = temp_gap_map['Time']
                    temp_gap.activated_URL = temp_gap_map['TabChanged']
                    temp_gap.gap_type = TAB_SWITCH_HRG
                #属性改NodeChanged
                elif key == 'NodeChanged':
                    temp_gap.clear()
                    temp_gap.time = temp_gap_map['Time']
                    temp_gap.changed_URL = temp_gap_map['NodeChanged']
                    temp_gap.gap_type = URL_UPDATED_HRG
                #增加click判定，属性为ClickAction
                elif key == 'ClickAction':
                    temp_gap.clear()
                    temp_gap.time = temp_gap_map['Time']
                    #更改参数
                    temp_gap.click_action = temp_gap_map['ClickAction']
                    temp_gap.click_element = temp_gap_map['ElementDetails']
                    temp_gap.gap_type = CLICK_ACTION_HRG
                #增加input判定，属性为InputAction
                elif key == 'InputAction':
                    temp_gap.clear()
                    temp_gap.time = temp_gap_map['Time']
                    #更改参数
                    temp_gap.input_action = temp_gap_map['InputAction']
                    temp_gap.input_element = temp_gap_map['InputDetails']
                    temp_gap.gap_type = INPUT_ACTION_HRG
            gap_append = HTTP_request_Gap()
            gap_append.deepcopy(temp_gap)
            HTTP_request_Gap_List.append(gap_append)
        print("HTTP_request_Gap_List", HTTP_request_Gap_List)
    return HTTP_request_Gap_List

ChromeExtensionLoader(example_file_path)
