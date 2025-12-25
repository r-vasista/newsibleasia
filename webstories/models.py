from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import os

def validate_vertical_image(file):
    """Validate image is vertical (720x1280 recommended)"""
    img = Image.open(file)
    width, height = img.size
    
    # Check if vertical (height > width)
    if height <= width:
        raise ValidationError(
            'Image must be vertical format. '
            'Recommended size: 720x1280 pixels. '
            f'Your image: {width}x{height}'
        )
    
    # Warn if not ideal size
    if width != 720 or height != 1280:
        pass  # Just log warning, don't block

def validate_image_size(file):
    """Validate image file size"""
    max_size_mb = getattr(settings, 'WEBSTORY_IMAGE_MAX_SIZE_MB', 5)
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file.size > max_size_bytes:
        current_size_mb = file.size / (1024 * 1024)
        raise ValidationError(
            f'Image file size is {current_size_mb:.2f}MB. '
            f'Maximum allowed is {max_size_mb}MB.'
        )

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
    """AMP Web Story Model"""
    category = models.ForeignKey(
        WebStoryCategory, 
        on_delete=models.CASCADE, 
        related_name='stories'
    )
    title = models.CharField(
        max_length=70,
        help_text="Story title (max 70 chars for SEO)"
    )
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    
    # Cover/Poster image (MUST be vertical 720x1280)
    poster_portrait = models.ImageField(
        upload_to='webstories/posters/',
        validators=[validate_image_size, validate_vertical_image],
        help_text="Vertical image 720x1280px (Required for AMP)"
    )
    
    # Publisher info (for AMP) - REQUIRED by Google
    publisher_name = models.CharField(
        max_length=100,
        default="Newsible",
        help_text="Publisher name for AMP stories (REQUIRED by Google AMP)"
    )
    
    # SEO Fields
    meta_description = models.TextField(
        max_length=160, 
        blank=True, 
        null=True,
        help_text="SEO meta description (150-160 characters)"
    )
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "AMP Web Stories"
        ordering = ['order', '-published_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Clean URL as per guidelines: /web-stories/story-slug/"""
        return f'/web-stories/{self.slug}/'
    
    def get_page_count(self):
        """Get number of pages"""
        return self.pages.count()
    
    def is_valid_for_publish(self):
        """Check if story meets minimum requirements"""
        page_count = self.get_page_count()
        if page_count < 5:
            return False, f"Need at least 5 pages (currently {page_count})"
        return True, "Ready to publish"


class WebStoryPage(models.Model):
    """AMP Web Story Page (Slide)"""
    
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    story = models.ForeignKey(
        WebStory, 
        on_delete=models.CASCADE, 
        related_name='pages'
    )
    
    # Media type choice
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image',
        help_text="Choose image or video for this page"
    )
    
    # Page image (MUST be vertical 720x1280)
    image = models.ImageField(
        upload_to='webstories/pages/',
        validators=[validate_image_size, validate_vertical_image],
        blank=True,
        null=True,
        help_text="Vertical image 720x1280px (Required if media type is Image)"
    )
    
    # Page video (MP4 format recommended)
    video = models.FileField(
        upload_to='webstories/videos/',
        blank=True,
        null=True,
        help_text="MP4 video file (vertical 720x1280 recommended, max 10MB)"
    )
    
    # Video poster/thumbnail (shown before video loads)
    video_poster = models.ImageField(
        upload_to='webstories/video_posters/',
        blank=True,
        null=True,
        validators=[validate_image_size, validate_vertical_image],
        help_text="Thumbnail for video (720x1280px, shown while video loads)"
    )
    
    # Page heading (short)
    heading = models.CharField(
        max_length=100,
        help_text="Short heading for this page"
    )
    
    # Page text (max 200 chars as per Google guidelines)
    text = models.TextField(
        max_length=200,
        help_text="Max 200 characters (Google recommendation)"
    )
    
    # Optional credit
    credit = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Photo/Video credit (e.g., 'Photo: Reuters' or 'Video: AFP')"
    )
    
    order = models.IntegerField(default=0)
    
    # Auto-advance duration (in seconds)
    duration = models.IntegerField(
        default=5,
        help_text="Duration in seconds before auto-advancing to next page (3-15 seconds recommended)"
    )
    
    # AMP layer template choice
    LAYOUT_CHOICES = [
        ('vertical', 'Vertical (Text at bottom)'),
        ('thirds', 'Thirds (Text in middle)'),
    ]
    layout = models.CharField(
        max_length=20,
        choices=LAYOUT_CHOICES,
        default='vertical',
        help_text="Text layout position"
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = "Story Page"
        verbose_name_plural = "Story Pages"
    
    def __str__(self):
        media = "Video" if self.media_type == 'video' else "Image"
        return f"{self.story.title} - Page {self.order} ({media})"
    
    def clean(self):
        """Validate page requirements"""
        super().clean()
        
        # Check text length
        if len(self.text) > 200:
            raise ValidationError({
                'text': 'Text must be 200 characters or less (Google guideline)'
            })
        
        # Validate media type requirements
        if self.media_type == 'image':
            if not self.image:
                raise ValidationError({
                    'image': 'Image is required when media type is Image'
                })
        elif self.media_type == 'video':
            if not self.video:
                raise ValidationError({
                    'video': 'Video file is required when media type is Video'
                })
            
            # Check video file size (max 10MB for performance)
            max_video_size = 10 * 1024 * 1024  # 10MB
            if self.video.size > max_video_size:
                size_mb = self.video.size / (1024 * 1024)
                raise ValidationError({
                    'video': f'Video size is {size_mb:.1f}MB. Maximum 10MB recommended for Web Stories performance.'
                })
    
    def save(self, *args, **kwargs):
        # Auto-optimize image to 720x1280 if needed
        super().save(*args, **kwargs)
        
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            
            # Resize to 720x1280 if different
            if img.size != (720, 1280):
                img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                img.save(img_path, quality=85, optimize=True)
        
        if self.video_poster:
            poster_path = self.video_poster.path
            img = Image.open(poster_path)
            
            # Resize poster to 720x1280 if different
            if img.size != (720, 1280):
                img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                img.save(poster_path, quality=85, optimize=True)
