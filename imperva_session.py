#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :imperva_session.py
# @Time      :2022/7/18 17:35

import base64

user = input("请输入账号:")
password = input("请输入密码:")

pwd = user + ":" + password

# 设置json格式
headers = {"content-type": "application/json"}

# 将pwd进行base64编码，因py3默认为utf-8格式，需解码utf-8
bs64_pwd = base64.b64encode(pwd.encode('utf-8')).decode('ascii')
print("你的Session值为: " + bs64_pwd)
