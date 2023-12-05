'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-29 15:49:08
LastEditTime: 2023-12-04 19:42:51
LastEditors: Suez_kip
Description: 
'''
import Tools.logger
from Tools.configloader import *

import codecs
def handleEncoding(original_file):
    #newfile=original_file[0:original_file.rfind(.)]+'_copy.csv'
    f=open(original_file,'rb+')
    content=f.read()#读取文件内容，content为bytes类型，而非string类型
    source_encoding='utf-8'
    #####确定encoding类型
    try:
        content.decode('utf-8').encode('utf-8')
        source_encoding='utf-8'
    except:
        try:
            content.decode('gbk').encode('utf-8')
            source_encoding='gbk'
        except:
            try:
                content.decode('gb2312').encode('utf-8')
                source_encoding='gb2312'
            except:
                try:
                    content.decode('gb18030').encode('utf-8')
                    source_encoding='gb18030'
                except:
                    try:
                        content.decode('big5').encode('utf-8')
                        source_encoding='gb18030'
                    except:
                        content.decode('cp936').encode('utf-8')
                        source_encoding='cp936'
    f.close()

if __name__ == "__main__":
    original_file = r"D:\Suez_kip\研究生毕设\Code\Test\Source\flow.txt"
    handleEncoding(original_file)