from django.contrib import admin
from service.models import SubscribeUser
from django.contrib.auth.models import User
import random

def ins_sub_job():
    #print('hello')
    num = random.randint(0,100)
    SubscribeUser.objects.create(num)
    #logger.info('Hello cron')
  