'''
Author: Suez_kip 287140262@qq.com
Date: 2024-04-02 10:01:03
LastEditTime: 2024-04-02 10:23:29
LastEditors: Suez_kip
Description: 
'''
import re

def filter_clicks_and_write_to_new_file(input_file_path, output_file_path):
    filtered_lines = []  # 存储符合条件的行
    pattern_1 = r"ActivatedURL: \{\s*\}"
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            #对ActivatedURL为{}的line进行过滤
            match_1 = re.search(pattern_1, line)
            if not match_1:
                continue
            else:
                filtered_lines.append(line)
    # 将筛选后的行写入新文件
    with open(input_file_path, 'r', encoding='utf-8') as file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in file:
                if line in filtered_lines:
                    continue
                else:
                    output_file.write(line)
        print("Filter Complete!")


#///////压缩input////////



if __name__ == "__main__":
    # 输入文件和输出文件的路径
    input_file_path = "./source/console.log"
    output_file_path = "./source/filtered_data.txt"

    # 执行函数，读取输入文件，筛选并写入输出文件
    filter_clicks_and_write_to_new_file(input_file_path, output_file_path)
