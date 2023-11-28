'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-28 15:43:46
LastEditTime: 2023-11-28 15:48:16
LastEditors: Suez_kip
Description: 
'''
import json

CONFIG_DICT = {}

class config_init :
    def __init__(self):
        self.get_config()

    def get_param_according_dict(self, target_dicts):
        for dict_key, dict_value in target_dicts.items():
            if "#" not in dict_key :
                CONFIG_DICT[dict_key] = dict_value

    def get_config(self):
        with open(r"default.json", encoding='utf-8') as f:
            dicts = json.load(f)
            self.get_param_according_dict(dicts)
            f.close()
        with open(r"config.json", encoding='utf-8') as f:
            dicts = json.load(f)
            self.get_param_according_dict(dicts)
            f.close()


if __name__ == "__main__":
    print("<CONFIG LOADER TEST>")
    loader = config_init()
    print(CONFIG_DICT)
    print("</CONFIG LOADER TEST>")