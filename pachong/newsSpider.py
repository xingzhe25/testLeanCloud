# newsSpider.py
# coding: utf-8

# import sys
# import os
# import urllib2
import requests
import re
#from lxml import etree
import random

# def StringListSave(save_path, filename, slist):
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     path = save_path + "/" + filename + ".txt"
#     with open(path, "w+") as fp:
#         for s in slist:
#             #print s[0].encode("utf8"), s[1].encode("utf8")
#             #print s
#             #break
#             fp.write("%s\t\t%s\n" %(s[0].encode("utf8"), s[1].encode("utf8")))

def page_info(myPage):
    '''Regex'''
    mypage_info = re.findall(r'<div class="subNav">.*?<a href=".*?">.*?</a></div>', myPage, re.S)
    mypage_info = re.findall(r'<a href="(.*?)">(.*?)</a>', mypage_info[0], re.S)
    return mypage_info

# def new_page_info(new_page):
#     # xpath
#     dom = etree.HTML(new_page)
#     new_items = dom.xpath('//tr/td/a/text()')
#     new_urls = dom.xpath('//tr/td/a/@href')
#     assert(len(new_items) == len(new_urls))
#     return zip(new_items, new_urls)

# def Spider(url):
#     i = 0
#     print "downloading ", url
#     myPage = requests.get(url).content.decode("gbk")
#     myPageResults = page_info(myPage)
#     #print myPageResults
#     save_path = 'wangyiNews'
#     filename = str(i) + "_" + u"新闻排行榜"
#     StringListSave(save_path, filename, myPageResults)

#     # 下一级
#     i += 1
#     for url, item in myPageResults:
#         print "downloading ", url
#         new_page = requests.get(url).content.decode("gbk")
#         newPageResults = new_page_info(new_page)
#         filename = str(i) + "_" + item
#         StringListSave(save_path, filename, newPageResults)
#         i += 1
#         #break
def getwangyi(url):
    content = "没获取到内容"
    print "downloading ", url
    myPage = requests.get(url).content.decode("gbk")
    myPageResults = page_info(myPage)
    url_list = []
    for next_url, item in myPageResults:
        #print "downloading ", next_url
        #new_page = requests.get(next_url).content.decode("gbk")
        #newPageResults = new_page_info(new_page)
        url_list.append(next_url)
    #print url_list

    xuanze = random.randint(0, len(url_list))
    content = url_list[xuanze]

    return content

# 爬取糗事百科
def getQiuShi(url):
    qsPage = requests.get(url).content.strip()
    qsResults = infoQiuShi(qsPage)
    return qsResults

def infoQiuShi(qsPage):
    qsInfos = re.findall(r'<div class="content">.*?<span>(.*?)</span>.*?</div>', qsPage, re.S)
    return qsInfos


if __name__ == '__main__':
    print 'start'

    start_url = 'https://www.qiushibaike.com/text/'
    #Spider(start_url)
    qsContent = getQiuShi(start_url)
    num = '2'
    try:
        if num.isdigit():
            num = int(num)
            res = qsContent[num] + qsContent[num + 1] + qsContent[num + 2]
            res = "请输入小于 %d 的整数." % num
        else:
            res = "请输入数字"
    except Exception as e:
        res = e
    print res
    
    print 'end'