
from django.contrib.sitemaps import Sitemap
#from blog.models import Entry
from post_management.models import NewsPost
from django.urls import reverse


class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return NewsPost.objects.filter(status='active').order_by('-id')

    def lastmod(self, obj):
        return obj.post_date
    
class StaticSitemap(Sitemap):
        
    def items(self):
        return ['about-us','contact-us','advertise-with-us','upcoming-events']

    def location(self, item):
        return reverse(item)