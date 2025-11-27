from django.contrib import admin
from .models import Journalist, Language, Equipment, Qualification, Gallery
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django import forms

class JournalistAdminForm(forms.ModelForm):
    facebook = forms.URLField(required=False, label="Facebook Profile")
    linkedin = forms.URLField(required=False, label="LinkedIn Profile")
    youtube = forms.URLField(required=False, label="YouTube Profile")
    instagram = forms.URLField(required=False, label="Instagram Profile")
    twitter = forms.URLField(required=False, label="Twitter Profile")
    globe = forms.URLField(required=False, label="websites")

    class Meta:
        model = Journalist
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.social_media_links:
            for key in self.instance.social_media_links.keys():
                if key in self.fields:
                    self.fields[key].initial = self.instance.social_media_links[key]

    def clean(self):
        cleaned_data = super().clean()
        social_media_links = {}

        for field in ["facebook", "linkedin", "youtube", "instagram", "twitter", "globe"]:
            if cleaned_data.get(field):
                social_media_links[field] = cleaned_data[field]

        cleaned_data["social_media_links"] = social_media_links
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.social_media_links = self.cleaned_data.get("social_media_links", {})
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class JournalistAdmin(admin.ModelAdmin):
    list_display = ('username', 'parent_organisations', 'registration_type', 'display_social_links', 'email', 'status', 'first_name', 'last_name', 'created_at')
    search_fields = ('username', 'parent_organisations', 'registration_type', 'first_name', 'last_name','email', 'phone_number', 'nationality__name')
    list_filter = ('status','registration_type',  'created_at')
    exclude = ("social_media_links",)
    raw_id_fields = ("city", "state", "nationality") 
    list_editable=['status']

    filter_horizontal = ('languages', 'selected_equipment') 

    def show_languages(self, obj):
        """Show selected languages in a separate column."""
        selected_languages = ", ".join([language.name for language in obj.languages.all()])
        return selected_languages if selected_languages else "No Selection"

    show_languages.short_description = "Selected Languages"

    def show_equipment(self, obj):
        """Show selected equipment in a separate column."""
        selected_equipment = ", ".join([equipment.name for equipment in obj.selected_equipment.all()])
        return selected_equipment if selected_equipment else "No Selection"

    show_equipment.short_description = "Selected Equipment"
    form = JournalistAdminForm

    def display_social_links(self, obj):
        """Show clickable social media links in admin list."""
        if not obj.social_media_links:
            return "No Links"

        links_html = ""
        for platform, url in obj.social_media_links.items():
            links_html += f'<a href="{url}" target="_blank">{platform.capitalize()}</a> | '
        
        return mark_safe(links_html[:-3])  # Remove last "|"

    display_social_links.short_description = "Social Media Links"

admin.site.register(Journalist, JournalistAdmin)


class LanguageAdimn(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(Language, LanguageAdimn)


class QualificationAdimn(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(Qualification, QualificationAdimn)

class EquipmentAdimn(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(Equipment, EquipmentAdimn)

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('journalist', 'status', 'post_at')
    search_fields = ['journalist__username', 'status', 'journalist__email']
admin.site.register(Gallery, GalleryAdmin)