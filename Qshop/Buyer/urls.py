from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [
    path('index/', index),
    re_path(r"^$", index),
    re_path(r"goods/(?P<id>\d+)/",goods),
    path('goods_list/',goods_list),
    path('cart/',cart),
    path('login/',login),
    path('register/',register),
    path('user_center_site/',user_center_site),
    path('user_center_order/',user_center_order),
    path('user_center_info/',user_center_info),
    path('place_order/', pay_order),
    path('get_pay/', get_pay),
    path('pay_result/', pay_result)
]
urlpatterns += [
    path('fileTest/',fileTest)
]