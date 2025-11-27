from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class seo_optimization(models.Model):
    pagename=models.CharField(max_length=255, verbose_name="Page Name",null=True,default=None)
    pageslug=models.CharField(max_length=160, verbose_name="Page Url",null=True,default=None)
    metatitle=models.CharField(max_length=75, verbose_name="Page Meta Title",null=True,default=None)
    metadescription=models.TextField(max_length=175, verbose_name="Page Meta Des",null=True,default=None)
    pagecontent=RichTextUploadingField(null=True,default='No News', verbose_name="Long Discretion")
    post_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 