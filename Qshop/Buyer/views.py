from django.shortcuts import render
from Shop.models import Goods,GoodsType
from django.http import HttpResponse,HttpResponseRedirect
import csv
from Shop.views import valid_user,set_password
from QUser.views import *

def index(request):
    # # 查询所有类型
    type_list = GoodsType.objects.all()
    # 查询单个类型
    type_data = GoodsType.objects.get(id = 1)
    # 查询对应类型的所有商品
    type_data.goods_set.all()
    # 查询每个类型的对应的商品
    for t in type_list:
        goods_list = t.goods_set.all()
    # 查询每个类型的对应的4个商品
    for t in type_list:
        goods_list = t.goods_set.all()[:4]
    # 上述内容进行整理
    result = [{t.name:t.goods_set.all(),"pic":t.picture} for t in type_list]
    message = "hello"
    return render(request,"buyer/index.html",locals())

def goods_list(request):
    id = request.GET.get("id")
    goods_list = GoodsType.objects.all()
    if id:
        goods_type = GoodsType.objects.get(id=int(id))
        goods_list = goods_type.goods_set.all()
    return render(request, "buyer/goods_list.html", {"goods_list":goods_list})

def goods(request, id):
    goods_data = Goods.objects.get(id = int(id))
    return render(request, "buyer/goods.html", locals())

def fileTest(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disponsiton'] = "attachment;filename=abc.csv"
    writer = csv.writer(response)
    writer.writerow(['username','age','height','weight'])
    writer.writerow(['zhiliao','18','180','100'])#在这里并不会指定文件名字.
    return response

def login_valid(fun):
    def inner(request,*args,**kwargs):
        referer = request.GET.get("referer")#证明使用者的目的地在购物车页面
        cookie_user = request.COOKIES.get("email")
        session_user = request.session.get("email")
        if cookie_user and session_user and cookie_user ==session_user:
            return fun(request,*args,**kwargs)
        else:
            login_url = "/Buyer/login/"
            if referer:
                login_url = "/Buyer/login/?referer=%s"%referer
            return HttpResponseRedirect(login_url)
    return inner

@login_valid
def cart(request):
    cookie_user = request.COOKIES.get("email")
    session_user = request.session.get("email")
    if cookie_user and session_user and cookie_user == session_user:
        return render(request, "buyer/cart.html")
    else:
        return HttpResponseRedirect("/Buyer/login/")

def pay_order(request):
    return render(request,"buyer/place_order.html")

import time
from Buyer.Pay import pay

def get_pay(request):
    order_number = str(time.time()).replace(".","")
    order_price = "666.66"
    url = pay(order_number,order_price)
    return HttpResponseRedirect(url)

def pay_result(request):
    data = request.GET
    return render(request, "buyer/pay_result.html",locals())

def login(request):
    #记录登陆请求是从哪里到的登陆页面
    referer = request.GET.get("referer")
    if not referer:
        referer = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        #判断用户是否存在
        #如果存在
        user = valid_user(email)
        if user:
            #判断密码是否正确
            db_password = user.password
            request_password = set_password(password)
            if db_password == request_password:
                if request.POST.get("referer"):
                    referer = request.POST.get("referer")
                if referer in ('http://127.0.0.1:8000/Buyer/login/',"None"):
                    referer = "http://127.0.0.1:8000/Buyer"
                # print(referer)
                # referer = request.POST.get("referer") 不要加这一行,这玩意儿是把referer替换掉的意思
                # print(referer)
                response = HttpResponseRedirect(referer)
                response.set_cookie("email",user.email)
                response.set_cookie("user_id",user.id)
                request.session["email"] = user.email
                return response
                # return HttpResponseRedirect("/Buyer/index/")
                # return render(request,"buyer/index.html")
            else:
                error = "密码错误"
        else:
            error = "用户不存在"
    return render(request,"buyer/login.html",locals())

def register(request):
    """
    后台卖家注册功能
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        #检测用户是否注册过
        #注册过,提示当前邮箱已经注册
        error = ""
        if valid_user(email):
            error = "当前邮箱已经注册"
        #没有注册过
        else:
            #对密码进行加密
            password = set_password(password)
            #保存数据库
            add_user(email = email, password = password)
            #跳转到登录页
            return HttpResponseRedirect("/buyer/login/")
    return render(request,"buyer/register.html")

def user_center_site(request):
    return render(request,"buyer/user_center_site.html")

def user_center_order(request):
    return render(request, "buyer/user_center_order.html")

def user_center_info(request):
    return render(request,"buyer/user_center_info.html")