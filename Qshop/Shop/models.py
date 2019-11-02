from django.db import models
from ckeditor.fields import RichTextField
from QUser.models import *

class GoodsTypeManager(models.Manager):
    def hello(self, id):
        return self.get(id=id).goods_set.all[:4]

class GoodsType(models.Model):
    name = models.CharField(max_length=32)
    picture = models.ImageField(upload_to = "shop/img",default="shop/img/1.jpg")
    objects = GoodsTypeManager()

class Goods(models.Model):
    name = models.CharField(max_length = 32)
    price = models.FloatField()
    number = models.IntegerField()
    production = models.DateTimeField(blank=True,null=True)
    safe_date = models.CharField(max_length = 32)
    picture = models.ImageField(upload_to = "shop/img",default="shop/img/1.jpg")
    description = RichTextField()

    statue = models.IntegerField(default=1)  # 0 下架 1 上架
    goods_type = models.ForeignKey(to=GoodsType,on_delete = models.CASCADE)
    goods_store = models.ForeignKey(to=Quser, on_delete=models.CASCADE)

