# coding: utf-8
import urllib2
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# soup = BeautifulSoup(html, "lxml")

# #print soup.prettify()
# print soup.title

#!/usr/bin/env python
# import thread
# import time

# def print_time(thread_name, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print "%s %s" %(thread_name, time.ctime(time.time()))

# try:
#     thread.start_new_thread(print_time, ("Thread-1", 2, ))
#     thread.start_new_thread(print_time, ("Thread-2", 4, ))
# except:
#     print "Error: unable to start the thread."

# while True:
#     pass

import re
import requests
import os

f = open('source.txt', 'r')
html = f.read()
f.close()
#print html

png_urls = re.findall('<img src="(.*?)"', html, re.S)
i = 0
path = 'pic'
if not os.path.exists(path):
    os.makedirs(path)
for png_url in png_urls:
    print "now downloading: " + png_url
    png = requests.get(png_url)
    
    fp = open(path + '\\' + str(i) + '.png', 'wb')
    fp.write(png.content)
    fp.close()
    i += 1