'''
Author: Suez_kip 287140262@qq.com
Date: 2023-12-21 13:54:59
LastEditTime: 2023-12-21 13:55:56
LastEditors: Suez_kip
Description: 
'''

import requests
from lxml import etree
from lxml import html
from html.parser import HTMLParser #导入html解析库
from selenium import webdriver
import time
 
def getHTMLText(url):
        driver = webdriver.PhantomJS(executable_path='E:\\pythontest\\phantomjs-2.1.1-windows\\bin\\phantomjs')  # phantomjs的绝对路径
        time.sleep(2)
        driver.get(url)  # 获取网页
        time.sleep(2)
        return driver.page_source
 
def getHtmlByXpath(html_str,xpath):
        strhtml = etree.HTML(html_str)
        strResult = strhtml.xpath(xpath)
        return strResult
 
def w_file(filepath,contents):
    with open(filepath,'w',encoding='gb18030') as wf:
        wf.write(contents)
         
def main():
    url = 'https://m.fygdrs.com/h5/news.html?t=2&id=67062' #要访问的网址
    strhtml = getHTMLText(url) #获取HTML
    #print(html)
    w_file('E:\\pythontest\\wfile.txt',strhtml)
    strDiv=getHtmlByXpath(strhtml,"//div[@id='Article-content']")
    if(strDiv):
        str1= html.tostring(strDiv[0])
        print(str1)
        str2 = HTMLParser().unescape(str1.decode())
        print(str2)
        w_file('E:\\pythontest\\wfile3.txt',str2)
        
    print('ok')
