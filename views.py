# coding: utf-8

from datetime import datetime

from django.http import HttpResponse
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
