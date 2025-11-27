from django.contrib import admin
from Seo_management.models import seo_optimization

# Register your models here.
class seo(admin.ModelAdmin):
    list_display=('pagename','pageslug','metatitle','metadescription','pagecontent','post_date')

admin.site.register(seo_optimization,seo)