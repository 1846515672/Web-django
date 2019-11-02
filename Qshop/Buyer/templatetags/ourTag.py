from django import template


register = template.Library()#实例化django模板库

@register.filter#注册过滤器
def uper(obj):#过滤方法
    """
    obj是被过滤的对象
    :param obj:
    :return:
    """
    return obj.uper()#过滤的结果

@register.filter
def get_four(obj):
    return obj[:4]

@register.filter
def get_filter(obj):
    """
    :param obj: 是一个查询的商品类型实例对象
    :return:
    """
    result = obj.goods_set.filter(statue=1)[:4]
    return result

@register.filter("rep_v1")
def get_rep(obj, a):
    a,b = a.split(",")
    return obj.replace(a, b)

@register.filter("rep")
def get_rep(obj, a):
    return obj.replace(a, a.upper())