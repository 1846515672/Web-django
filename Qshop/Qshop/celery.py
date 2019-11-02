from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# 设置celery的工作目录
os.environ.setdefault('DJANGO_SETTNGS_MODULE', "CeleryTask.settings")
# 实例化celery
app = Celery('Project')
    # celery服务具体的名称
# celery配置的来源
app.config_from_object('django.conf:settings')
#如果在app当中有创建task.py,就会自动检索
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
