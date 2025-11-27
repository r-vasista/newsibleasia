from django.contrib import admin
from .models import CMS, profile_setting
from django.utils.html import format_html
from django import forms


class cmsadmin(admin.ModelAdmin):
    list_display=('pagename', 'slug', 'post_date', 'updated_at', 'viewcounter', 'post_status', 'order')
    search_fields=('pagename','slug')
    list_filter=('post_date','order')
    readonly_fields = ('viewcounter',)
    list_editable=('post_status','order',)
    cropping_fields = {'image_crop': ('pageimage',)}
admin.site.register(CMS,cmsadmin)


class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = profile_setting
        fields = '__all__'
        widgets = {
            'background_theme_light': forms.TextInput(attrs={'type': 'color'}),
            'background_theme_dark': forms.TextInput(attrs={'type': 'color'}),
            'container_background': forms.TextInput(attrs={'type': 'color'}),
            'items_background': forms.TextInput(attrs={'type': 'color'}),
        }

class profile_settingAdmin(admin.ModelAdmin):
    form = ProfileSettingForm
    list_display = ('id', 'create_date', 'updated_at', 'status')
    search_fields = ('id', 'create_date', 'updated_at',)
    list_filter = ('create_date',)
    list_editable = ['status']
    readonly_fields = ['main_office_map', 'branch_office_map', 'create_date', 'updated_at']
    cropping_fields = {'image_crop': ('pageimage',)}

    def main_office_map(self, obj):
        if obj.main_office_address:
            url = f"https://www.google.com/maps/search/?api=1&query={obj.main_office_address.replace(' ', '+')}"
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.main_office_address)
        return "-"
    main_office_map.short_description = "Main Office Map"

    def branch_office_map(self, obj):
        if obj.branch_office_address:
            url = f"https://www.google.com/maps/search/?api=1&query={obj.branch_office_address.replace(' ', '+')}"
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.branch_office_address)
        return "-"
    branch_office_map.short_description = "Branch Office Map"


    fieldsets = (
        ('Logos, image & Theme', {
            'fields': (
                'logo_light', 'logo_dark',
                'footer_img', 'body_img',
                'background_theme_light', 'background_theme_dark', 'container_background', 'items_background',
            )
        }),
        ('Contact Info', {
            'fields': (
                'phone_number1', 'phone_number2',
                'email',
            )
        }),
        ('Social Media', {
            'fields': (
                'facbook', 'instagram', 'twitter', 'linkedin', 'youtube',
            )
        }),
        ('Office Addresses', {
            'fields': (
                'main_office_address', 'main_office_map',
                'branch_office_address', 'branch_office_map',
            )
        }),
        ('Metadata', {
            'fields': (
                'establish_at', 'google_map',
                'copyright', 'status', 'author',
                'create_date', 'updated_at',
            )
        }),
    )
admin.site.register(profile_setting, profile_settingAdmin)