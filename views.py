# coding: utf-8

from datetime import datetime
import random

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from leancloud import Object
from leancloud import Query
from leancloud.errors import LeanCloudError

# wexin
import hashlib
from django.views.decorators.csrf import csrf_exempt
import time
from django.template import loader, Context
from xml.etree import ElementTree as ET
from wechat_sdk.basic import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

# pacong
from pachong.newsSpider import page_info
import requests

# 中文支持
import sys
reload(sys)
sys.setdefaultencoding('utf8')

WECHAT_TOKEN = '1db18532c43ec91f39b6448a865f4096'
# 实例化 WechatBasic
wechat_instance = WechatBasic(token=WECHAT_TOKEN)

class Todo(Object):
    pass


def index(request):
    return render(request, 'index.html', {})


def current_time(request):
    return HttpResponse(datetime.now())


class TodoView(View):
    def get(self, request):
        try:
            todos = Query(Todo).descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:  # 服务端对应的 Class 还没创建
                todos = []
            else:
                raise e
        return render(request, 'todos.html', {
            'todos': [x.get('content') for x in todos],
        })

    def post(self, request):
        content = request.POST.get('content')
        todo = Todo(content=content)
        try:
            todo.save()
        except LeanCloudError as e:
            return HttpResponseServerError(e.error)
        return HttpResponseRedirect(reverse('todo_list'))

class hiWechat(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(hiWechat, self).dispatch(*args, **kwargs)

    def get(self, request):
        # 接收为信服务器参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        token = '1db18532c43ec91f39b6448a865f4096'

        # 序列化
        hashlist = [token, timestamp, nonce]
        hashlist.sort()

        # 合成一个字符串
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()

        # 比较
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return ""


    # def post(self, request):
    #     str_xml = ET.fromstring(request.body)

    #     fromUser = str_xml.find('ToUserName').text
    #     toUser = str_xml.find('FromUserName').text
    #     content = str_xml.find('Content').text
    #     createTime = str_xml.find('CreateTime').text

    #     # 获取当前时间
    #     nowtime = str(init(time.time()))

    #     t = loader.get_template('text.xml')
    #     c = Context({'toUser': toUser, 'fromUser': fromUser,
    #         'nowtime': 1503562682, 'content': 'hi'})

    #     return HttpResponse(t.render(c))

    def post(self, request):
        try:
            wechat_instance.parse_data(data = request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')

        # 获取解析好的微信请求信息
        message = wechat_instance.get_message()

        if isinstance(message, TextMessage):
            # 当前会话内容
            content = message.content.strip()
            print "**content: " + content
            #content = getwangyi("http://news.163.com/rank/")            
            wangyiLink = self.getwangyi(url="http://news.163.com/rank/")
            print "**wangyiLink: " + wangyiLink

            response = wechat_instance.response_text(content=wangyiLink)

        else:
            response = wechat_instance.response_text(content="功能升级中")


        return HttpResponse(response, content_type="application/xml")

    def getwangyi(self, url):
        content = '没获取到内容'
        #print "downloading ", url
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
