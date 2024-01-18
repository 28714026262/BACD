'''
Author: Suez_kip 287140262@qq.com
Date: 2024-01-18 16:25:05
LastEditTime: 2024-01-18 16:25:10
LastEditors: Suez_kip
Description: 
'''

import datetime

def date_string_to_milliseconds(date_string: str):
    dt = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    milliseconds = int(dt.timestamp()*1000 + 499)
    return milliseconds

date_string = "2024-01-18 12:00:00"
milliseconds = date_string_to_milliseconds(date_string=date_string)
print(milliseconds)