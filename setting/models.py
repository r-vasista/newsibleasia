from django.db import models
from autoslug import AutoSlugField
from image_cropping import ImageCropField, ImageRatioField
from PIL import Image
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class CMS(models.Model):
    pagename=models.CharField(max_length=150, verbose_name="Page Name",null=True,default=None)
    Content=RichTextUploadingField(null=True,default='No News', verbose_name="Long Discretion")
    pageimage = ImageCropField(upload_to='cms/', max_length=255, null=True, blank=True, verbose_name="Page Image (1280X220px)")
    
    def save(self, *args, **kwargs):
        super(CMS, self).save(*args, **kwargs)
        if self.pageimage:
            img = Image.open(self.pageimage.path)
            desired_size = (1280, 220)
            img.thumbnail(desired_size)
            img.save(self.pageimage.path)
    
    slug=AutoSlugField(max_length=200, populate_from='pagename',unique=True,null=True,default=None)
    post_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewcounter = models.IntegerField(unique=False,null=True,default=0,verbose_name="Views")
    post_status=models.IntegerField(verbose_name="Counter",null=True,default=100)
    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='setting_cms_entries') 
    
    def __str__(self):
        return self.pagename
    
    def get_absolute_url(self):
         return reverse('cms', args=[self.slug])
    
    class Meta:
        ordering = ['order']
        verbose_name = "Content Management System"  


class profile_setting(models.Model):
    logo_light = models.ImageField(upload_to='logo/', null=True, blank=True, verbose_name="Logo Light (500X100px)")
    logo_dark = models.ImageField(upload_to='logo/', null=True, blank=True, verbose_name="Logo Dark (500X100px)")
    footer_img = models.ImageField(upload_to='profile_image/', null=True, blank=True, verbose_name="Footer Image (1920X365px)")
    body_img =  models.ImageField(upload_to='profile_image/', null=True, blank=True, verbose_name="Body Image (1920X365px)")
    background_theme_light = models.CharField(max_length=7, null=True, blank=True, default="#FFFFFF", verbose_name="background Theme Light", help_text="Light Background")
    background_theme_dark = models.CharField(max_length=7, null=True, blank=True, default="#000000", verbose_name="background Theme Dark", help_text="Dark Background")
    container_background = models.CharField(max_length=7, null=True, blank=True, default="#fcf8e7", verbose_name="container background", help_text="container background in body")
    items_background = models.CharField(max_length=7, null=True, blank=True, default="#FFFFFF", verbose_name="Items background", help_text="items background in body")
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number1 = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone Number 1")
    phone_number2 = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone Number 2")
    facbook = models.URLField(null=True, blank=True, verbose_name="Facebook")
    instagram = models.URLField(null=True, blank=True, verbose_name="Instagram")
    twitter = models.URLField(null=True, blank=True, verbose_name="Twitter")
    linkedin = models.URLField(null=True, blank=True, verbose_name="Linkedin")
    youtube = models.URLField(null=True, blank=True, verbose_name="Youtube")
    main_office_address = models.TextField(max_length=200, null=True, blank=True, verbose_name="Main Office Address")
    branch_office_address = models.TextField(max_length=255, null=True, blank=True, verbose_name="Branch Office Address")
    google_map = models.TextField(null=True, blank=True, verbose_name="Google Map", help_text="Embed Code")
    copyright = models.CharField(max_length=255, null=True, blank=True, verbose_name="Copyright")
    establish_at = models.DateField(null=True, blank=True, verbose_name="Establish At")
    create_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='setting_entries') 
    
    class Meta:
        verbose_name = "Profile Setting"
    
    def __str__(self):
        return str(self.id)