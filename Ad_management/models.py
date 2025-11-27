from django.db import models
from autoslug import AutoSlugField



class ad_category(models.Model):
    ads_cat_name=models.CharField(verbose_name="Ad Type",max_length=255,unique=True,null=True,default=None)
    ads_cat_slug=AutoSlugField(populate_from='ads_cat_name',unique=True,null=True,default=None)
    ads_cat_status=models.IntegerField(null=True,default=0)
    
    def __str__(self):
        return self.ads_cat_name

class ad(models.Model):
    ads_cat=models.ForeignKey("ad_category", verbose_name="Select Ad Type",null=True,default=None,on_delete=models.CASCADE)
    ad_url=models.CharField(max_length=255, verbose_name="Link URL",null=True,default=None)
    STATUS_CHOICES = (
        ('stil', 'Image'),
        ('video', 'Video'),
    )
    ad_type = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', verbose_name="Ad Type")
    from_date=models.DateField()
    to_date=models.DateField()
    ad_image = models.FileField(upload_to='ads/')
    ad_counter=models.IntegerField(verbose_name="Counter",null=True,default=None)
    is_active=models.BooleanField(verbose_name="Is Active", default=False)
    post_date=models.DateTimeField(auto_now=True)
    post_status=models.IntegerField(null=True,default=0)