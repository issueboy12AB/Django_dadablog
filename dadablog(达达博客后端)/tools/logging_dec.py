from django.http import JsonResponse
from django.conf import settings
import jwt
from user.models import UserProfile


def logging_check(func):
    def wrap(request, *args, **kwargs):

        # 获取token request.META.get('HTTP_AUTHORIZATION')
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)
        # 校验jwt
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KET)
        except Exception as e:
            print('jwt decode error is %s' % (e))
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)

        # 获取登录用户
        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap


def get_user_by_request(request):
    # 尝试性获取登录用户
    # return UserProfile obj or None
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY)
    except Exception as e:
        return None

    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user
