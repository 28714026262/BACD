import re

def filter_clicks_and_write_to_new_file(input_file_path, output_file_path):
    filtered_lines = []  # 存储符合条件的行
    valid_id_pattern = re.compile(r"id: '(h\d|H\d)'")
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "ClickDetected" in line and "ElementDetails" in line:
                # 提取ElementDetails部分
                start_idx = line.find("ElementDetails: {") + len("ElementDetails: {")
                end_idx = line.find("}", start_idx)
                element_details_str = line[start_idx:end_idx+1]

                # 尝试解析elementDetails中的tagName
                if "tagName: 'DIV'" in element_details_str:
                    # 使用正则表达式检查id是否符合条件
                    #if valid_id_pattern.search(element_details_str) or "id: 'main'" in element_details_str or "id: ''" in element_details_str:
                    if "id: ''" in element_details_str:
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



# 输入文件和输出文件的路径
input_file_path = "C:/Users/User/Downloads/BACD/BACD-main/source/console.log"
output_file_path = "C:/Users/User/Downloads/BACD/BACD-main/source/filtered_data.txt"

# 执行函数，读取输入文件，筛选并写入输出文件
filter_clicks_and_write_to_new_file(input_file_path, output_file_path)