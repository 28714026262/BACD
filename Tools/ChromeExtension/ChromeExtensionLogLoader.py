import copy

example_file_path = r'D:\Suez_kip\研究生毕设\Data\29.20.130.39___jiangsuer1qaz#EDC\console-1705557139277.txt'

TAB_SWITCH_HRG = 1
URL_UPDATED_HRG = 2

class HTTP_request_Gap:
    def __init__(self) -> None:
        self.time = -1
        self.activated_URL = ""
        self.changed_URL = ""
        self.gap_type = -1
    
    def clear(self):
        self.time = -1
        self.activated_URL = ""
        self.changed_URL = ""
        self.gap_type = -1
    
    def deepcopy(self, new_gap):
        self.time = new_gap.time
        self.activated_URL = copy.deepcopy(new_gap.activated_URL)
        self.changed_URL = copy.deepcopy(new_gap.changed_URL)
        self.gap_type = new_gap.gap_type

def ChromeExtensionLoader(file_path = example_file_path):
    HTTP_request_Gap_List = []
    INIT_FLAG = True
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        temp_gap = HTTP_request_Gap()
        temp_gap_map = {}
        NEW_GAP_FLAG = True
        for line in lines:
            first_space_index = line.find(' ')
            result = (line[first_space_index + 1:]).strip()
            if result == "NEW_LOG_START":
                if INIT_FLAG:
                    INIT_FLAG = False
                else:
                    if 'ActivatedURL' in temp_gap_map:
                        temp_gap.clear()
                        temp_gap.time = temp_gap_map["Time"]
                        temp_gap.activated_URL = temp_gap_map["ActivatedURL"]
                        temp_gap.gap_type = TAB_SWITCH_HRG
                    elif "URLChanged" in temp_gap_map:
                        temp_gap.clear()
                        temp_gap.time = temp_gap_map["Time"]
                        temp_gap.changed_URL = temp_gap_map["URLChanged"]
                        temp_gap.gap_type = URL_UPDATED_HRG
                    gap_append = HTTP_request_Gap()
                    gap_append.deepcopy(temp_gap)
                    HTTP_request_Gap_List.append(gap_append)

                    temp_gap_map = {}
            elif ":" in result:
                kv_pair = result.split(": ")
                kv_pair[1] = kv_pair[1][1:len(kv_pair[1])-1]
                temp_gap_map[kv_pair[0]] = kv_pair[1]

    print(HTTP_request_Gap_List)
    return HTTP_request_Gap_List

ChromeExtensionLoader()