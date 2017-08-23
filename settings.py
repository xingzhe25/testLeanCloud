# coding: utf-8

import os

DEBUG = os.environ.get('LEANCLOUD_APP_ENV') != 'production'
ROOT_URLCONF = 'urls'
#SECRET_KEY = 'replace-this-with-your-secret-key'
SECRET_KEY = 'i7htv7k^=hxl-8uho4pf$)uurkcc3wfxs((cg6+l#k57vgl4zl'
ALLOWED_HOSTS = ['*']

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['templates'],
}]

# weixin
WECHAT_TOKEN = "1db18532c43ec91f39b6448a865f4096"
WEIXIN_APPID = 'wxe6905834d4ca57db'
WEIXIN_APPSECRET = '39dff12902ea3555c2f3a2ecb99c6469'
