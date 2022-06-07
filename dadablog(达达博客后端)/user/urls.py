from django.urls import path

from . import views

urlpatterns = [
    # 短信
    path('sms', views.sms_view),
    path('<str:username>',views.UserViews.as_view()), # 用户详情路由
    path('<str:username>/avatar',views.users_views), # 用户信息修改路由
]