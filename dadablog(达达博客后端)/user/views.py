import json
import random

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from tools.logging_dec import logging_check
from tools.sms import YunTongXin
from user.models import UserProfile
import hashlib


# 异常码 10100 - 10199

# 注册、用户详情页
# from user.tasks import send_sms_c


class UserViews(View):

    def get(self, request, username=None):  # 用户信息详情
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                result = {'code': 10102, 'error': 'User name already exists.'}
                return JsonResponse(result)
            result = {'code': 200,'username': username,'data': {'info': user.info,'sign': user.sign,'nickname': user.nickname,'avatar': str(user.avatar)}}
            return JsonResponse(result)
        else:
            pass

        return JsonResponse({'code': 200, 'msg': 'test'})

    def post(self, request):  # 注册
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        sms_num = json_obj['sms_num']

        # 两次密码是否一致
        if password_1 != password_2:
            result = {'code': 10100, 'error': 'Two passwords are different.'}
            return JsonResponse(result)

        # 比对验证码是否一致
        old_code = cache.get('sms_%s'%(phone))
        if not old_code:
            result = {'code':'10110', 'error':'The code is wrong'}
            return JsonResponse(result)
        if int(sms_num) != old_code:
            result = {'code':'10111', 'error':'The code is wrong'}
            return JsonResponse(result)

        # 判断用户名唯一
        old_users = UserProfile.objects.filter(username=username)
        if old_users:
            result = {'code': 10101, 'error': 'User name already exists.'}
            return JsonResponse(result)

        # 密码md5加密
        p_m = hashlib.md5()
        p_m.update(password_1.encode())

        UserProfile.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email,phone=phone)

        result = {'code': 200, 'username': username, 'data': {}}
        return JsonResponse(result)

    @method_decorator(logging_check)
    def put(self, request, username=None):
        # 更新用户信息数据
        json_str = request.body
        json_obj = json.loads(json_str)

        user = request.myuser

        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']
        user.save()
        return JsonResponse({'code': 200})


# 用户信息修改页
@logging_check
def users_views(request, username):
    if request.method != 'POST':
        result = {'code': 10103, 'error': 'Please use POST'}
        return JsonResponse(result)

    user = request.myuser

    avatar = request.FILES['avatar']
    user.avatar = avatar
    user.save()
    return JsonResponse({'code': 200})


def sms_view(request):
    if request.method != 'POST':
        result = {'code': 10108, 'error': 'Please use POST'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']
    # 生成随机码
    code = random.randint(1000, 9999)
    print('phone', phone, 'code', code)
    # 储存随机码 django-redis
    cache_key = 'sms_%s' % (phone)
    # 检查是否有已经发过且未过期的验证码
    old_code = cache.get(cache_key)
    if old_code:
        return JsonResponse({'code': 10111, 'error': 'The code is already existed'})

    cache.set(cache_key, code, 60)
    # 发送随机码 -> 短信
    send_sms(phone, code)
    # celery模式
    # send_sms_c.delay(phone, code)
    return JsonResponse({'code': 200})


def send_sms(phone, code):
    config = {
        'accountSid': '8a216da8804ba8a501804eff4ea80089',
        'accountToken': '6d6a78bc1605425f8a7d8970bdc3cd97',
        'appId': '8a216da8804ba8a501804eff4fa4008f',
        'templateId': '1',
    }
    yun = YunTongXin(**config)
    res = yun.run(phone, code)
    return res
