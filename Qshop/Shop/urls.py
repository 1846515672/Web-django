from django.urls import path, re_path,include
from Shop.views import *

urlpatterns = [
    re_path(r"^$", index),#默认匹配index
    path("index/",index),
    path("register/", register),
    path("login/", login),
    path("logout/", logout),
    path("forgot_password/", forgot_password),
    path('reset_password/', reset_password),
    path('change_password/', change_password),
    path('profile/', profile),
    path('ckeditor/',include("ckeditor_uploader.urls")),
    path("add_goods/", add_goods),
    path('list_goods/', list_goods),
    re_path(r"^set_goods/(?P<id>\d+)/", set_goods),
    re_path(r'^goods/(?P<id>\d+)/', goods),
    path('set_profile/', set_profile),
    path("all_select/",all_select)
]
urlpatterns += [
    path('get_celery/',get_celery),
    path('blank/',blank),
    path('vue_list_goods/',vue_list_goods),
    path("Goods/",GoodsView.as_view()),
    path("vue_list_goods/",vue_list_goods),
    path('change_goods/',change_goods),
    re_path(r'^change_goods/(?P<id>\d+)/',change_goods),
    re_path(r'^update_goods/(?P<id>\d+)/',update_goods),
    path('example/',example),
]