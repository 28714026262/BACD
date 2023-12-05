'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-29 15:49:08
LastEditTime: 2023-12-05 15:43:17
LastEditors: Suez_kip
Description: 
'''
import os
import sys
sys.path.append(os.getcwd())

from Tools.configloader import *
from Tools.logger import get_logger
logger = get_logger(name = os.path.basename(__file__))
def handleEncoding(content):
    return_str = ""
    encoding_type = 'utf-8'
    try:
        return_str = content.decode(encoding_type)
        encoding_type = 'gbk'
    except:
        try:
            return_str = content.decode('gbk')
            encoding_type = 'gb2312'
        except:
            try:
                return_str = content.decode('gb2312')
                encoding_type = 'gb18030'
            except:
                try:
                    return_str = content.decode('gb18030')
                    encoding_type = 'big5'
                except:
                    try:
                        return_str = content.decode('big5')
                        encoding_type = 'cp936'
                    except:
                        try:
                            return_str = content.decode('cp936')
                        except:
                            logger.debug("No Decode Type Valid!")
                            logger.debug(content)
    return return_str