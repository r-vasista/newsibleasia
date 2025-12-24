from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import WebStory

class WebStorySitemap(Sitemap):
    """
    Separate sitemap for AMP Web Stories
    URL: /sitemap-webstories.xml
    """
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        """Return only published stories"""
        return WebStory.objects.filter(is_published=True).order_by('-published_date')
    
    def lastmod(self, obj):
        """Return last modification date"""
        return obj.updated_at
    
    def location(self, obj):
        """Return clean URL"""
        return obj.get_absolute_url()
