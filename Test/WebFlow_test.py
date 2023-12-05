'''
Author: Suez_kip 287140262@qq.com
Date: 2023-11-29 11:13:14
LastEditTime: 2023-12-04 10:23:15
LastEditors: Suez_kip
Description: 
'''
import sys
sys.path.append("D:\Suez_kip\研究生毕设\Code") 
from WebFSM.WebFlow import *
from Tools.RequestsAnalyser.HTMLRequestAnalyzer.HTMLRequestAnalyzer import *

example_str_req = r"D:\Suez_kip\研究生毕设\Code\Test\Source\PostRequest.txt"
example_str_resp = r"D:\Suez_kip\研究生毕设\Code\Test\Source\PostResponse.txt"
example_str_req_not_path = r"""POST /jaccount/ulogin HTTP/1.1
Host: jaccount.sjtu.edu.cn
Connection: close
Content-Length: 1041
Cache-Control: max-age=0
sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://jaccount.sjtu.edu.cn
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://jaccount.sjtu.edu.cn/jaccount/jalogin?sid=jaoauth220160718&client=CO401UhaKf%2FN1eJmNCA4wiIrEj8rpybtoGfTzR51nCZh&returl=CCNh6YOGTaMpCF7jL%2BPuWR%2F0f2XEmB%2FSJDseV4w04fM0yjjUGDF7lExwH%2FnoaimXzDUEM0htJJHCDBl4OZynQAr0PZM1ne9fSSWnfpofgN0u5OK8%2B2P6kqdfa2Od%2BfJxmy24%2FBIXJqmtqY4Ny6G%2B6q0%3D&se=CIYH%2BnoXC728F3FKsmwxRLz1qWB1ss4Qa%2BIh8Cy0p7jegDTnBEqKevPE06D%2B33pQxHZGUhrN4jHV
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=537AFFE33D795F1F799D25E18B6A3226.jaccount105; _ga=GA1.3.573489039.1682647241; _ga_5G709VBQWD=GS1.3.1697082313.1.1.1697082322.0.0.0; Qs_lvt_374225=1698650048; Qs_pv_374225=1981948842915752000; jaoauth2021=ffffffff09701c6345525d5f4f58455e445a4a4229a0; jajaccount2021=ffffffff09701c7845525d5f4f58455e445a4a4229a0; _gid=GA1.3.1268188298.1701315985; _gat=1; _ga_QP6YR9D8CK=GS1.3.1701315985.11.0.1701315985.0.0.0

sid=jaoauth220160718&returl=CCNh6YOGTaMpCF7jL%2BPuWR%2F0f2XEmB%2FSJDseV4w04fM0yjjUGDF7lExwH%2FnoaimXzDUEM0htJJHCDBl4OZynQAr0PZM1ne9fSSWnfpofgN0u5OK8%2B2P6kqdfa2Od%2BfJxmy24%2FBIXJqmtqY4Ny6G%2B6q0%3D&se=CIYH%2BnoXC728F3FKsmwxRLz1qWB1ss4Qa%2BIh8Cy0p7jegDTnBEqKevPE06D%2B33pQxHZGUhrN4jHV&v=&uuid=2dcce77a-bd30-4c33-9a02-a1958ed6cacc&client=CO401UhaKf%2FN1eJmNCA4wiIrEj8rpybtoGfTzR51nCZh&user=122036910037&pass=szk10101&captcha=vuprp&g-recaptcha-response=03AFcWeA6xocF8ubEapz1PaiSTOgBDrVrSaWMFIF1f8Ei7VIsu0JygNhUeQzA3ivxD4PAC4mHnKwaEGECmdRHsrUTb3qBl72HGMkY8dKpjYduv1vJQuGAY5EZmY2EzWJ_mt3ndFcs9LdFKLr0kz0vA_tepvuH9PpSE6oX0v6bsCTM0yhbt-Mg8RU7nPwF6J-WzwQd5GEmq935J7sW8LyUtL6ydVvgXBTK24ENeXJGL2h7G_7-tA-BqHi3AWx4gLhUK1rk86JgpaP-YjFVSltzB9PFe4LcBqIHDBo0C1zsQgFuo76g4pcTYJghBO9dO27nQ4GVHcAb7eJbDaDTkY7XsY98eAKqZt28JagrPHuvh-Ew_wNqNgX9jg2doLgTqC7KXqGxWHRHeWd5HSLLiIzWGaa-p5mvxo3wvB3l5wGQQOflJcWxC8oUnA4IBd4TU49zfxRf_E9tucEK2Hnt-phM-XZiqVQcC9SB4eZ6lqhiL0G_7b_zuuL_pQwDd_htIfIH-yMaj0iXXEF43xoOfGx-4X0lYWD2NLBoqNy_718fcZt6vWuBSsd7sOidkc0Af8UyXqyfvwSRoem07"""

def test1():
    # Request Test
    GFNA = Global_Flow_Node_Analyser()
    GFNA.getHRAInStr(example_str_req_not_path, "")
    GFNA.getDataFromTraffic()
    
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
    GFNA.getHRAInPath(example_str_req, example_str_resp)
    GFNA.getDataFromTraffic()
    
    assert GFNA.g_flow_node_container.response.status == '200'
    assert GFNA.g_flow_node_container.response.status_str == 'OK'
    headers_list = [{'name': 'Date', 'value': 'Sun, 03 Dec 2023 04:01:16 GMT'}, 
                    {'name': 'Server', 'value': 'nginx/1.23.4'}, 
                    {'name': 'Content-Type', 'value': 'text/javascript; charset=utf-8'}, 
                    {'name': 'Content-Disposition', 'value': 'inline; filename=performance.js'}, 
                    {'name': 'Last-Modified', 'value': 'Mon, 25 Sep 2023 07:29:06 GMT'}, 
                    {'name': 'Cache-Control', 'value': 'no-cache'}, 
                    {'name': 'ETag', 'value': '"1695626946.5698967-2881-299961987-gzip"'}, 
                    {'name': 'Access-Control-Allow-Origin', 'value': '*'}, 
                    {'name': 'Access-Control-Allow-Headers', 'value': 'Content-Type, Authorization'}, 
                    {'name': 'Access-Control-Allow-Methods', 'value': 'OPTIONS, HEAD, GET, POST, DELETE, PUT'}, 
                    {'name': 'Vary', 'value': 'Accept-Encoding'}, 
                    {'name': 'Content-Length', 'value': '2881'}, 
                    {'name': 'Connection', 'value': 'close'}]
    for index in range(0, len(GFNA.g_flow_node_container.response.headers_array())):
        assert GFNA.g_flow_node_container.response.headers_list[index]['name'] == headers_list[index]['name']
        assert GFNA.g_flow_node_container.response.headers_list[index]['value'] == headers_list[index]['value']

if __name__ == "__main__":
    test1()