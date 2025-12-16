from django.contrib import admin
from .models import WebStoryCategory, WebStory, WebStorySlide

class WebStorySlideInline(admin.TabularInline):
    model = WebStorySlide
    extra = 1
    fields = ['order', 'media_type', 'image', 'video', 'video_url', 'description', 'duration']

@admin.register(WebStoryCategory)
class WebStoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(WebStory)
class WebStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'author', 'is_published', 'views', 'published_date']
    list_filter = ['category', 'is_published', 'published_date']
    list_editable = ['is_published']
    search_fields = ['title', 'category__name']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [WebStorySlideInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'thumbnail', 'author')
        }),
        ('Publishing', {
            'fields': ('is_published', 'order')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )

@admin.register(WebStorySlide)
class WebStorySlideAdmin(admin.ModelAdmin):
    list_display = ['story', 'order', 'media_type', 'duration']
    list_filter = ['media_type', 'story__category']
    search_fields = ['story__title', 'description']
    list_editable = ['order']