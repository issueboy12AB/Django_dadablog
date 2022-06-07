import hashlib
import json
import time

import jwt
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# 异常码：10200-10299
from dadablog import settings
from user.models import UserProfile

# 登录
def tokens(request):
    if request.method != 'POST':
        result = {'code': 10200, 'error': 'Please use POST!'}
        return JsonResponse(result)
    # 查询数据
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']

    # 判断用户名是否存在
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        result = {'code': 10201, 'error': 'User name does not exist'}
        return JsonResponse(result)

    # 判断密码是否正确
    p_m = hashlib.md5()
    p_m.update(password.encode())

    if p_m.hexdigest() != user.password:
        result = {'code': 10202, 'error': 'Or wrong user name and password'}
        return JsonResponse(result)

    # 设置令牌token
    token = make_token(username)
    result = {'code': 200, 'username': username, 'data': {'token':token.decode()}}
    return JsonResponse(result)


def make_token(username, expire=3600 * 24): # 创建用户令牌
    key = settings.JWT_TOKEN_KET
    now_t = time.time()
    payload_data = {'username': username, 'exp': now_t + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')
