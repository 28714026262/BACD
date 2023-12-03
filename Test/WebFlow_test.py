'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-29 11:13:14
LastEditTime: 2023-12-03 17:28:31
LastEditors: Suez_kip
Description: 
'''
import sys
sys.path.append("D:\Suez_kip\研究生毕设\Code") 
from WebFSM.WebFlow import *
from Tools.RequestsAnalyser.HTMLRequestAnalyzer.HTMLRequestAnalyzer import *

example_str_req = r"D:\Suez_kip\研究生毕设\Code\Test\Source\PostRequest.txt"
example_str_resp = r"D:\Suez_kip\研究生毕设\Code\Test\Source\PostResponse.txt"

def test1():
    # Request Test
    GFNA = Global_Flow_Node_Analyser()
    GFNA.getDataFromTrafficwithRequestPath(example_str_req, example_str_resp)
    
    assert GFNA.g_flow_node_container.content_type == 'application/x-www-form-urlencoded'
    assert GFNA.g_flow_node_container.method == "POST"
    target_result_dict = {'sid': 'jaoauth220160718', 
                            'returl': 'CCNh6YOGTaMpCF7jL+PuWR/0f2XEmB/SJDseV4w04fM0yjjUGDF7lExwH/noaimXzDUEM0htJJHCDBl4OZynQAr0PZM1ne9fSSWnfpofgN0u5OK8+2P6kqdfa2Od+fJxmy24/BIXJqmtqY4Ny6G+6q0=', 
                            'se': 'CIYH+noXC728F3FKsmwxRLz1qWB1ss4Qa+Ih8Cy0p7jegDTnBEqKevPE06D+33pQxHZGUhrN4jHV', 
                            'v': '', 
                            'uuid': '2dcce77a-bd30-4c33-9a02-a1958ed6cacc', 
                            'client': 'CO401UhaKf/N1eJmNCA4wiIrEj8rpybtoGfTzR51nCZh', 
                            'user': '122036910037', 
                            'pass': 'szk10101', 
                            'captcha': 'vuprp', 
                            'g-recaptcha-response': '03AFcWeA6xocF8ubEapz1PaiSTOgBDrVrSaWMFIF1f8Ei7VIsu0JygNhUeQzA3ivxD4PAC4mHnKwaEGECmdRHsrUTb3qBl72HGMkY8dKpjYduv1vJQuGAY5EZmY2EzWJ_mt3ndFcs9LdFKLr0kz0vA_tepvuH9PpSE6oX0v6bsCTM0yhbt-Mg8RU7nPwF6J-WzwQd5GEmq935J7sW8LyUtL6ydVvgXBTK24ENeXJGL2h7G_7-tA-BqHi3AWx4gLhUK1rk86JgpaP-YjFVSltzB9PFe4LcBqIHDBo0C1zsQgFuo76g4pcTYJghBO9dO27nQ4GVHcAb7eJbDaDTkY7XsY98eAKqZt28JagrPHuvh-Ew_wNqNgX9jg2doLgTqC7KXqGxWHRHeWd5HSLLiIzWGaa-p5mvxo3wvB3l5wGQQOflJcWxC8oUnA4IBd4TU49zfxRf_E9tucEK2Hnt-phM-XZiqVQcC9SB4eZ6lqhiL0G_7b_zuuL_pQwDd_htIfIH-yMaj0iXXEF43xoOfGx-4X0lYWD2NLBoqNy_718fcZt6vWuBSsd7sOidkc0Af8UyXqyfvwSRoem07'}
    for key in GFNA.g_flow_node_container.params_post:
        assert target_result_dict[key] == GFNA.g_flow_node_container.params_post[key]
    assert GFNA.g_flow_node_container.url == '/jaccount/ulogin'

def test2():
    # Response Test
    GFNA = Global_Flow_Node_Analyser()
    GFNA.getDataFromTrafficwithRequestPath(example_str_req, example_str_resp)
    
    assert GFNA.g_flow_node_container.response.status == '200'
    assert GFNA.g_flow_node_container.response.status_str == 'OK'
    headers_list = [{'name': 'Date', 'value': 'Sun, 03 Dec 2023 04:01:16 GMT'}, {'name': 'Server', 'value': 'nginx/1.23.4'}, {'name': 'Content-Type', 'value': 'text/javascript; charset=utf-8'}, {'name': 'Content-Disposition', 'value': 'inline; filename=performance.js'}, {'name': 'Last-Modified', 'value': 'Mon, 25 Sep 2023 07:29:06 GMT'}, {'name': 'Cache-Control', 'value': 'no-cache'}, {'name': 'ETag', 'value': '"1695626946.5698967-2881-299961987-gzip"'}, {'name': 'Access-Control-Allow-Origin', 'value': '*'}, {'name': 'Access-Control-Allow-Headers', 'value': 'Content-Type, Authorization'}, {'name': 'Access-Control-Allow-Methods', 'value': 'OPTIONS, HEAD, GET, POST, DELETE, PUT'}, {'name': 'Vary', 'value': 'Accept-Encoding'}, {'name': 'Content-Length', 'value': '2881'}, {'name': 'Connection', 'value': 'close'}]
    for index in range(0, len(GFNA.g_flow_node_container.response.headers_array())):
        assert GFNA.g_flow_node_container.response.headers_list[index]['name'] == headers_list[index]['name']
        assert GFNA.g_flow_node_container.response.headers_list[index]['value'] == headers_list[index]['value']

if __name__ == "__main__":
    test2()