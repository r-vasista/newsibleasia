from django.contrib import admin
from Ad_management.models import ad_category
from Ad_management.models import ad
# Register your models here.


class Ad_category(admin.ModelAdmin):
    list_display=('id','ads_cat_name','ads_cat_slug','ads_cat_status')
admin.site.register(ad_category,Ad_category)

class Ad_post(admin.ModelAdmin):
    list_display=('ads_cat','ads_cat_id','ad_type','ad_url','ad_image','from_date','to_date','ad_counter','is_active')
    list_editable=('is_active',)

admin.site.register(ad,Ad_post)