from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class WebStoryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Web Story Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class WebStory(models.Model):
    category = models.ForeignKey(WebStoryCategory, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    thumbnail = models.ImageField(upload_to='webstories/thumbnails/')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Web Stories"
        ordering = ['-published_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/webstories/{self.category.slug}/{self.slug}'


class WebStorySlide(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    story = models.ForeignKey(WebStory, on_delete=models.CASCADE, related_name='slides')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='webstories/slides/', blank=True, null=True)
    video = models.FileField(upload_to='webstories/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or external video URL")
    description = models.TextField(max_length=500)
    order = models.IntegerField(default=0)
    duration = models.IntegerField(default=5, help_text="Duration in seconds for auto-play")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.story.title} - Slide {self.order}"