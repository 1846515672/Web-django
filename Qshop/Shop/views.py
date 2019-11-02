from django.shortcuts import render
from QUser.views import *
from django.http import HttpResponseRedirect,HttpResponse
from CeleryTask.tasks import add #导入要执行的任务
from CeleryTask.tasks import sendMial as SDM
import smtplib
from email.mime.text import MIMEText
from Shop.models import *
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from Qshop.settings import PAZE_SIZE
from Shop.models import GoodsType

def blank(request):
    return render(request, "Shop/blank.html")
# 校验登录
def login_valid(fun):
    def inner(request, *args, **kwargs):
        referer = request.GET.get("referer")#证明使用者的目的地在购物车页面
        cookie_user = request.COOKIES.get("email")
        session_user = request.session.get("email")
        if cookie_user and session_user and cookie_user == session_user:
            return fun(request, *args, **kwargs)
        else:
            login_url = "/Buyer/login/"
            if referer:
                login_url = "/Buyer/login/?referer=%s"%referer
            return HttpResponseRedirect(login_url)
    return inner

def register(request):
    """
    后台卖家注册功能
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # 检测用户是否注册过
        # 注册过,提示当前邮箱已经注册
        error = ""
        if valid_user(email):
           error = "当前邮箱已经注册"
        #没有注册过
        else:
            #对密码加密
            password = set_password(password)
            #保存数据库
            add_user(email = email, password = password)
            # 跳转到登陆
            return HttpResponseRedirect("/Shop/login/")
    return render(request,"Shop/register.html")

def login(request):
    """
    后台卖家登陆功能
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        #判断用户是否存在
        #如果存在
        user = valid_user(email)
        if user:
            # 判断密码是否正确
            db_password = user.password
            request_password = set_password(password)
            if db_password == request_password:
                response = HttpResponseRedirect("/Shop/")
                response.set_cookie("email", user.email)
                response.set_cookie("user_id", user.id)
                request.session["email"] = user.email
                return response
            else:
                error = "密码错误!"
        else:
            error = "用户不存在"
    return render(request, "Shop/login.html", locals())

@login_valid
def index(request):
    """
    后台卖家首页
    :param request:
    :return:
    """
    return render(request, "Shop/index.html")

def logout(request):
    """
    后台卖家退出登陆功能
    :param request:
    :return:
    """
    response = HttpResponseRedirect("/Shop/login/")
    response.delete_cookie("email")
    response.delete_cookie("user_id")
    request.session.clear()
    return response

def forgot_password(request):
    """
    后台卖家忘记密码功能
    :param request:
    :return:
    """
    return render(request, "Shop/forgot_password.html")

def reset_password(request):
    """
    重置密码
    1、接受发过来的邮箱，进行校验
    """
    if request.method == "POST":
        email = request.POST.get("email")
        if email and valid_user(email): #校验请求的邮箱是否有权限修改密码
            #发送邮件的内容
            #首先需要有找回页面的地址
            #其次包含要修改密码的账号
            #再次包含修改是的一个校验码
                #使用当前时间+账号 ==> md5加密
            hash_code = set_password(email)  #如果有权限，对邮箱进行hash加密生成校验值(在修改的时候确定修改身份)
            content = "http://127.0.0.1:8000/Shop/change_password/?email=%s&token=%s"%(email,hash_code) #将邮箱和加密的识别码传入url，形成一个新的含有get请求的修改密码链接，链接指向修改密码页面
            #发送邮件的步骤
            try:
                sendMial(content,email)
            except Exception as e:
                print(e)
            print(content)
    return HttpResponseRedirect("/Shop/forget_password/")


def change_password(request):
    """
    当前是否有资格修改密码
    :param request:
    :return:
    """
    if request.method == "POST":
        password = request.GET.get("password")
        email = request.COOKIES.get("change_email")

        e = Quser.objects.get(email=email)
        e.password = set_password(password)
        e.save()
        return HttpResponseRedirect("/Shop/login/")
    # 通过get请求获得了修改密码
    email = request.GET.get("email")
    token = request.GET.get("token")
    # 再次进项校验
    now_token = set_password(email)
    #当前提交人存在,并且token值正确
    if valid_user(email) and now_token == token:
        # 返回修改密码页面
        response = render(request, "Shop/change_password.html")
        response.set_cookie("change_email", email)
        return response
    else:
        return HttpResponseRedirect("/Shop/forgot_password/")

def sendMial(content, email):
    from Qshop.settings import MAIL_SENDER,MATL_PASSWORD,MAIL_SERVER,MAIL_PORT

    content = """请确认是否是本人,请点击下方链接进行修改密码
    <a href="%s">点击确认</a>"""%content
    print(content)
    #构建邮件格式
    message = MIMEText(content, "html" "utf-8")

    message["To"] = email
    message["From"] = MAIL_SERVER
    message["Subject"] = "密码修改"

    #发送邮件
    smtp = smtplib.SMTP_SSL(MAIL_SENDER, MAIL_PORT)
    smtp.login(MAIL_SENDER, MATL_PASSWORD)
    smtp.sendmail(MAIL_SENDER, [email], message.as_string())
    smtp.close()

def get_celery(request):
    x = 1
    y = 2
    add.delay(x, y)#调用celery任务使用的  启动任务
    SDM.delay("hello word", "2719929303@qq.com")#调用celery任务使用的
    return HttpResponse("调用完成")

@login_valid
def profile(request):
    """
    个人中心
    :param request:
    :return:
    """
    user_email = request.COOKIES.get("email")
    user = Quser.objects.get(email=user_email)

    return render(request, "Shop/profile.html", {"user":user})

@login_valid
def set_profile(request):
    """
    个人中心
    """
    user_email = request.COOKIES.get("email")
    user = Quser.objects.get(email=user_email)
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        gender = post_data.get("gender")
        age = post_data.get("age")
        phone = post_data.get("phone")
        address = post_data.get("address")
        picture = request.FILES.get("picture")

        user.username = username
        user.gender = gender
        user.age = age
        user.phone = phone
        user.address = address
        user.picture = picture
        user.save()
        return HttpResponseRedirect("/Shop/profile/")
    return render(request, "Shop/set_profile.html", {'user':user})

def base(request):
    return render(request,'Shop/base.html')

@login_valid
def add_goods(request):
    if request.method == "POST":
        post_data = request.POST
        name = post_data.get("name")
        price = post_data.get("price")
        number = post_data.get("number")
        safe_date = post_data.get("safe_date")
        production = post_data.get("production")
        description = post_data.get("description")
        picture = request.FILES.get("picture")

        goods = Goods()
        goods.name = name
        goods.price = price
        goods.number = number
        goods.production = production
        goods.description = description
        goods.safe_date = safe_date
        goods.picture = picture
        goods.save()
        return HttpResponseRedirect("/Shop/list_goods/")
    return render(request, 'Shop/add_goods.html')

def list_goods(request):
    email = request.COOKIES.get("email")
    user = Quser.objects.get(email=email)
    goods_list = Goods.objects.all()
    return render(request, "Shop/list_goods.html" ,locals())

def set_goods(request, id):
    """
    :param id:锁定商品的标识
    :param set_type: up上架 down下架
    """
    set_type = request.GET.get("set_type")
    goods = Goods.objects.filter(id = int(id))
    if set_type == "up":
        goods.update(statue = 1)
    elif set_type == "down":
        goods.update(statue=2)
    return HttpResponseRedirect("/Shop/list_goods/")


def goods(request, id):
    goods_data = Goods.objects.get(id=id)
    return render(request, "Shop/goods.html", locals())

class GoodsView(View):
    def get(self, request):
        result = {
            "version": "v1",
            "code": "200",
            "data": [],
            "page_range":[],
            "referer":""
        }
        id = request.GET.get("id")#尝试获取前端get提交的id
        # 如果id存在,获取当前id的数据
        if id:
            goods_data = Goods.objects.get(id=int(id))
            result["data"].append(
                {   "id":goods_data.id,
                    "name":goods_data.name,
                    "price":goods_data.price,
                    "number":goods_data.number,
                    "production":goods_data.production,
                    "safe_date":goods_data.safe_date,
                    "picture":goods_data.picture.url,
                    "description":goods_data.description,
                    "statue":goods_data.statue,
                }
            )
        #如果id不存在,获取所有数据
        else:
            #尝试获取页码,如果页码不存在,默认是第一页
            page_number = request.GET.get("page", 1)
            #尝试获取查询的值
            keywords = request.GET.get("keywords")
            #获取所有数据
            all_goods = Goods.objects.all()
            if keywords: #如果有值,查询对应值
                all_goods = Goods.objects.filter(name__contains=keywords)
                result["referer"] = "&keywords=%s"%keywords
            #进行分页
            paginator = Paginator(all_goods, PAZE_SIZE)
            #获取单页数据
            page_data = paginator.page(page_number)
            #获取页码
            result["page_range"] = list(paginator.page_range)
            #对当前数据进行遍历,形成字典,可进行json封装
            goods_data = [{"name":g.name,
                           "id":g.id,
                           "price":g.price,
                           "number":g.number,
                           "production":g.production,
                           "safe_date":g.safe_date,
                           "description":g.description,
                           "statue":g.statue
                           }
                          for g in page_data
                          ]
            result["data"] = goods_data
        return JsonResponse(result)

@login_valid
def vue_list_goods(request):
    return render(request, "Shop/vue_list_goods.html")


def all_select(request):
    type = request.GET.get("type")
    goods_list = Goods.objects.all()
    for goods in goods_list:
        if goods.statue == 0:
            goods.statue = 1
            goods.save()
        elif goods.statue == 1:
            goods.statue = 0
            goods.save()
        else:
            goods.statue = 1
            goods.save()
    # for goods in goods_list:
    #     if goods.statue == 0:
    #         goods.statue=1
    #         goods.save()
    #     else:
    #         goods.statue=0
    #         goods.save()
    return HttpResponseRedirect('/Shop/list_goods/')


@login_valid
def change_goods(request, id=0):
    type_list = GoodsType.objects.all()
    if id:
        goods_data = Goods.objects.get(id=id)
    else:
        goods_data = Goods()
    if request.method == "POST":
        post_data = request.POST
        name = post_data.get("name")
        price = post_data.get("price")
        number = post_data.get("number")
        production = post_data.get("production")
        safe_date = post_data.get("safe_date")
        description = post_data.get("description")
        picture = request.FILES.get("picture")
        goods_type = post_data.get("goods_type")

        goods_data.name = name
        goods_data.price = price
        goods_data.number = number
        goods_data.production = production.replace("年","-").\
            replace("月","-").replace("日","-")
        goods_data.safe_date = safe_date
        goods_data.description = description
        #保存商品类型
        goods_data.goods_type = GoodsType.objects.get(id=int(goods_type))
        #保存商店
        #获取cookie当中的店铺
        store_id = request.COOKIES.get("email")
        #获取店铺信息
        goods_data.goods_store = Quser.objects.get(email=store_id)
        if picture:
            goods_data.picture = picture
        goods_data.save()
        return HttpResponseRedirect("/Shop/goods/%s/"%goods_data.id)
    return render(request, "Shop/change_goods.html", locals())

def update_goods(request, id):
    goods_data = Goods.objects.get(id=id)
    if request.method == "POST":
        post_data = request.POST
        name = post_data.get("name")
        price = post_data.get("price")
        number = post_data.get("number")
        production = post_data.get("production")
        picture = request.FILES.get("picture")
        safe_date = post_data.get("safe_date")
        description = post_data.get("description")

        goods_data.name = name
        goods_data.price = price
        goods_data.number = number
        goods_data.production = production.replace("年","-").replace("月","-").replace("日","")
        goods_data.safe_date = safe_date
        goods_data.description = description
        if picture:
            goods_data.picture = picture
        goods_data.save()
        return HttpResponseRedirect("/Shop/goods/%s/"%id)
    return render(request,"Shop/update_goods.html",locals())

def example(request):
    # method = dir(request)
    # request.META.get("HTTP_REFERER")#请求的来源
    all_data = GoodsType.objects.all()
    four_goods = GoodsType.objects.hello(1)
    return render(request,"Shop/Example.html",locals())

