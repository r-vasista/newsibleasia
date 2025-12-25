from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import WebStory, WebStoryCategory, WebStoryPage

class WebStoryPageInline(admin.TabularInline):
    model = WebStoryPage
    extra = 5
    fields = ('order', 'media_type', 'heading', 'text', 'image', 'video', 'video_poster', 'duration', 'credit', 'layout')
    ordering = ['order']
    
    class Media:
        css = {
            'all': ('admin/css/webstory_admin.css',)
        }
        js = ('admin/js/webstory_admin.js',)

@admin.register(WebStoryCategory)
class WebStoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'story_count', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def story_count(self, obj):
        count = obj.stories.filter(is_published=True).count()
        return f"{count} stories"
    story_count.short_description = "Published Stories"

@admin.register(WebStory)
class WebStoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'category', 
        'page_count_badge',
        'is_published', 
        'views', 
        'published_date',
        'preview_link'
    )
    list_filter = ('is_published', 'category', 'published_date')
    list_editable = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'validation_status')
    
    fieldsets = (
        ('Story Information', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Cover Image', {
            'fields': ('poster_portrait',),
            'description': 'Upload vertical image (720x1280px) - Required for AMP'
        }),
        ('Publisher Info', {
            'fields': ('publisher_name',),
            'description': 'Publisher name is REQUIRED by Google AMP specification'
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'order', 'views')
        }),
        ('Validation', {
            'fields': ('validation_status',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [WebStoryPageInline]
    
    def page_count_badge(self, obj):
        count = obj.get_page_count()
        color = 'green' if count >= 5 else 'red'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{} pages</span>',
            color,
            count
        )
    page_count_badge.short_description = "Pages"
    
    def validation_status(self, obj):
        is_valid, message = obj.is_valid_for_publish()
        color = 'green' if is_valid else 'red'
        return format_html(
            '<div style="color: {}; font-weight: bold;">{}</div>',
            color,
            message
        )
    validation_status.short_description = "Validation Status"
    
    def preview_link(self, obj):
        if obj.is_published:
            url = obj.get_absolute_url()
            return format_html(
                '<a href="{}" target="_blank" style="color: #417690;">View Story →</a>',
                url
            )
        return "-"
    preview_link.short_description = "Preview"
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(WebStoryPage)
class WebStoryPageAdmin(admin.ModelAdmin):
    list_display = ('story', 'order', 'media_type', 'heading', 'duration', 'text_preview', 'layout')
    list_filter = ('story', 'media_type', 'layout')
    search_fields = ('story__title', 'heading', 'text')
    list_editable = ('order',)
    
    fieldsets = (
        ('Media Selection', {
            'fields': ('story', 'order', 'media_type'),
            'description': 'Choose whether this page uses an image or video'
        }),
        ('Image Settings', {
            'fields': ('image',),
            'description': 'Upload if media type is Image (720x1280px)',
            'classes': ('collapse',)
        }),
        ('Video Settings', {
            'fields': ('video', 'video_poster'),
            'description': 'Upload video (MP4) and optional poster image',
            'classes': ('collapse',)
        }),
        ('Page Content', {
            'fields': ('heading', 'text', 'credit', 'layout')
        }),
        ('Auto-Advance', {
            'fields': ('duration',),
            'description': 'Duration in seconds before auto-advancing to next page'
        }),
    )
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Text Preview"
    
    class Media:
        js = ('admin/js/webstory_page_admin.js',)
        