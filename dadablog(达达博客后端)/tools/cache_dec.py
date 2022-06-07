from django.core.cache import cache

from tools.logging_dec import get_user_by_request


def cache_set(expire):
    def _cache_set(func):
        def wrapper(request, *args, **kwargs):
            # 区分场景，只做列表页
            if 't_id' in request.GET:
                return func(request, *args, **kwargs)

            # 生成正确的cache_key【访客访问和博主访问】
            visitor_user = get_user_by_request(request)
            visitor_username = None
            if visitor_user:
                visitor_username = visitor_user.username
            author_username = kwargs['author_id']
            print('visitor is %s' % (visitor_username))
            print('author is %s' % (author_username))
            full_path = request.get_full_path()  # 获取带参路由
            if author_username == visitor_username:
                cache_key = 'topics_cache_self_%s' % (full_path)
            else:
                cache_key = 'topics_cache_%s' % (full_path)
            print(cache_key)
            # 判断是否有缓存，会缓存直接返回
            res = cache.get(cache_key)
            if res:
                print('cache in ')
                return res
            # 执行视图
            res = func(request, *args, **kwargs)
            # 储存缓存 cache对象set/get
            cache.set(cache_key, res, expire)
            # 返回响应
            return res

        return wrapper

    return _cache_set
