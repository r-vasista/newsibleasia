from django.db import models

from autoslug import AutoSlugField

from image_cropping import ImageCropField, ImageRatioField

from PIL import Image

from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField

from django.utils import timezone

from django.urls import reverse

from django.contrib.auth.models import User

from journalist.models import Journalist



class category(models.Model):

    cat_name=models.CharField(max_length=255,unique=True,null=True,default=None)

    cat_slug=AutoSlugField(populate_from='cat_name',unique=True,null=True,default=None)

    STATUS_CHOICES = (

        ('active', 'Active'),

        ('inactive', 'Inactive'),

    )

    cat_status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', verbose_name="Status")

    order=models.IntegerField(unique=True,null=True,default=None,verbose_name="Order")

    def __str__(self):

        return self.cat_name



class sub_category(models.Model):

    sub_cat=models.ForeignKey("category", verbose_name="Select Cetegory",null=True,default=None,on_delete=models.CASCADE)

    subcat_name=models.CharField(max_length=255,unique=True,null=True,default=None)

    subcat_slug=AutoSlugField(populate_from='subcat_name',unique=True,null=True,default=None)

    subcat_tag=models.TextField(null=True,default="#trending #latest", verbose_name="Cat tag")

    STATUS_CHOICES = (

        ('active', 'Active'),

        ('inactive', 'Inactive'),

    )

    subcat_status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', verbose_name="Status")

    order=models.IntegerField(unique=True,null=True,default=None,verbose_name="Order")

    def __str__(self):

        return self.sub_cat.cat_name + " / " + self.subcat_name

    

class NewsPost(models.Model):

    post_cat=models.ForeignKey("sub_category", verbose_name="Select Cetegory",null=True,default=None,on_delete=models.CASCADE)

    post_title=models.CharField(max_length=150, verbose_name="News Head Line",null=True,default=None)

    post_short_des=models.CharField(max_length=160, verbose_name="Short Discretion",null=True,default=None)

    post_des=RichTextUploadingField(null=True,default='No News', verbose_name="Long Discretion")

    # post_image=models.FileField(upload_to="blog/", max_length=255,null=True,default=None)

    post_image = ImageCropField(upload_to='blog/%Y/%m/%d', max_length=255,null=True,default=None, verbose_name="News Image (1280X720px)")

    #image_crop = ImageRatioField('post_image', '430x360')

    

    def save(self, *args, **kwargs):

        # Override the save method to resize the image before saving

        super(NewsPost, self).save(*args, **kwargs)

        # Open the image

        img = Image.open(self.post_image.path)

        # Set the desired size for cropping (width, height)

        desired_size = (1280, 720)

        # Resize the image while maintaining the aspect ratio

        img.thumbnail(desired_size)

        # Save the resized image back to the original path

        img.save(self.post_image.path)

    

    slug=AutoSlugField(max_length=200, populate_from='post_title',unique=True,null=True,default=None)

    post_tag=models.TextField(null=True,default="#trending #latest", verbose_name="News tag")

        

    is_active=models.BooleanField(verbose_name="Latest News", null=True, default=True)

    Head_Lines=models.BooleanField(verbose_name="Head Lines", null=True, default=False)

    articles=models.BooleanField(verbose_name="Articles", null=True, default=False)

    trending=models.BooleanField(verbose_name="Trending", null=True, default=False)

    BreakingNews=models.BooleanField(verbose_name="Breaking News", null=True, default=False)

    Event=models.BooleanField(verbose_name="Upcoming Event", null=True, default=False)

    

    Event_date=models.DateField(unique=False,null=False,default=timezone.now,verbose_name="Event Start Date")

    Eventend_date=models.DateField(unique=False,null=False,default=timezone.now,verbose_name="Event End Date")

    schedule_date=models.DateTimeField(unique=False,null=False,default=timezone.now,verbose_name="Schedule Date")

    post_date=models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    viewcounter = models.IntegerField(unique=False,null=True,default=0,verbose_name="Views", editable=False)

    post_status=models.IntegerField(verbose_name="Counter",null=True,default=100)

    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")

    STATUS_CHOICES = (

        ('active', 'Active'),

        ('inactive', 'Inactive'),

        ('rejected', 'Rejected'),

    )

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE, null=True, blank=True, default=None)



    def get_posted_by(self):

        if self.journalist:

            return self.journalist.username

        elif self.author:

            return self.author.username

        return "Unknown"



    def clean(self):

        from django.core.exceptions import ValidationError

        if not self.author and not self.journalist:

            raise ValidationError("A post must have either an author or a journalist.")

        if self.author and self.journalist:

            raise ValidationError("A post cannot have both an author and a journalist.")

    

    def __str__(self):

        return self.post_title

    

    def get_absolute_url(self):

         return reverse('newsdetails', args=[self.slug])

        



class VideoNews(models.Model):

    News_Category =models.ForeignKey("sub_category", verbose_name="Select Category",null=True,default=None,on_delete=models.CASCADE)

    VIDEO_CHOICES = (

        ('video', 'Video'),

        ('reel', 'Reel'),

    )

    video_type = models.CharField(max_length=8, choices=VIDEO_CHOICES, default='video', verbose_name="Video Type")

    video_title=models.CharField(max_length=150, verbose_name="Title (Lenth 60 Char)",null=True,default=None)

    slug=AutoSlugField(populate_from='video_title',unique=True,null=True,default=None)

    video_short_des=models.CharField(max_length=160, verbose_name="Meta/Short Des",null=True,default=None)

    video_des=RichTextUploadingField(null=True,default=None, verbose_name="Video Discretion")

    video_url=models.CharField(verbose_name="Youtube Video URL",max_length=255,default=True,null=True)

    video_thumbnail = ImageCropField(upload_to='thumbnail/%Y/%m/%d', max_length=255,null=True,default='thumbnail/na.jpg',blank=True, verbose_name="Thumbnail (1280X720px)")

    video_tag=models.CharField(max_length=255,null=True,default=0)

    schedule_date=models.DateTimeField(unique=False,null=False,default=timezone.now,verbose_name="Schedule Date")

    video_date=models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    viewcounter = models.IntegerField(unique=False,null=True,default=0,verbose_name="Views", editable=False)

    counter = models.IntegerField(unique=False,null=True,default=0,verbose_name="counter")

    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")

    Head_Lines=models.BooleanField(verbose_name="Head Lines", null=True, default=False)

    articles=models.BooleanField(verbose_name="Articles", null=True, default=False)

    trending=models.BooleanField(verbose_name="Trending", null=True, default=False)

    BreakingNews=models.BooleanField(verbose_name="Breaking News", null=True, default=False)

    STATUS_CHOICES = (

        ('active', 'Active'),

        ('inactive', 'Inactive'),

        ('rejected', 'Rejected'),

    )

    is_active = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', verbose_name="Status")

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE, null=True, blank=True, default=None)



    def get_posted_by(self):

        if self.journalist:

            return self.journalist.username

        elif self.author:

            return self.author.username

        return "Unknown"



    def clean(self):

        from django.core.exceptions import ValidationError

        if not self.author and not self.journalist:

            raise ValidationError("A post must have either an author or a journalist.")

        if self.author and self.journalist:

            raise ValidationError("A post cannot have both an author and a journalist.")

        

    def __str__(self):

        return self.video_title

    

    def get_absolute_url(self):

        return reverse('videonewsdetails', args=[self.slug])

     

class slider(models.Model):

    slidercat=models.ForeignKey("sub_category", verbose_name="Select Cetegory",null=True,default=None,on_delete=models.CASCADE)

    title=models.CharField(max_length=200, verbose_name="News Head Line",null=True,default=None)

    des=models.CharField(max_length=300, verbose_name="Short Discretion",null=True,default=None)

    sliderimage = ImageCropField(upload_to='blog/', max_length=255,null=True,default=None, verbose_name="Slider Image (1400X520px)")

    #image_crop = ImageRatioField('post_image', '430x360')

    

    def save(self, *args, **kwargs):

        # Override the save method to resize the image before saving

        super(slider, self).save(*args, **kwargs)

        # Open the image

        img = Image.open(self.sliderimage.path)

        # Set the desired size for cropping (width, height)

        desired_size = (1400, 520)

        # Resize the image while maintaining the aspect ratio

        img.thumbnail(desired_size)

        # Save the resized image back to the original path

        img.save(self.sliderimage.path)

    

    slug=AutoSlugField(max_length=200, populate_from='slidercat',unique=True,null=True,default=None)

    post_date=models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")

    STATUS_CHOICES = (

        ('active', 'Active'),

        ('inactive', 'Inactive'),

    )

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 

    

    def __str__(self):

        return self.slidercat

    