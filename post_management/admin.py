from django.contrib import admin
from post_management.models import category, sub_category, NewsPost, VideoNews, slider,Tag,CMS
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from django.contrib.admin import SimpleListFilter


class Post_cat(admin.ModelAdmin):
    list_display=('cat_name','cat_slug','cat_status','order')
    list_editable=('cat_status','order',)
admin.site.register(category,Post_cat)

class Post_subcat(admin.ModelAdmin):
    list_display=('subcat_name','subcat_slug','sub_cat','subcat_status','order','subcat_tag')
    list_editable=('subcat_status','order',)
    list_filter=('subcat_status','sub_cat','order')
admin.site.register(sub_category,Post_subcat)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','is_active','create_date')
    search_fields = ('name',)
admin.site.register(Tag,TagAdmin)

class TopViewedFilter(SimpleListFilter):
    title = 'Reach (Views)'
    parameter_name = 'viewcounter'

    def lookups(self, request, model_admin):
        return [
            ('>500', 'Above 500 views'),
            ('>800', 'Above 800 views'),
            ('>1000', 'Above 1000 views'),
            ('>1500', 'Above 1500 views'),
            ('>2000', 'Above 2000 views'),
            ('>2000', 'Above 2500 views'),
            ('>2000', 'Above 3000 views'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '>500':
            return queryset.filter(viewcounter__gt=500)
        if self.value() == '>800':
            return queryset.filter(viewcounter__gt=800)
        if self.value() == '>1000':
            return queryset.filter(viewcounter__gt=1000)
        if self.value() == '>1500':
            return queryset.filter(viewcounter__gt=1500)
        if self.value() == '>2000':
            return queryset.filter(viewcounter__gt=2000)
        if self.value() == '>2500':
            return queryset.filter(viewcounter__gt=2500)
        if self.value() == '>3000':
            return queryset.filter(viewcounter__gt=3000)

class Post_Admin(admin.ModelAdmin):
    search_fields = (
        'post_title', 
        'author__username', 
        'author__first_name', 
        'author__last_name', 
        'journalist__username', 
        'journalist__first_name', 
        'journalist__last_name', 
        'journalist__organisation_name', 
        'slug',
        'post_cat__subcat_name',
        'post_date',
        'post_image',
        'tags__name'  # ✅ Use tags instead of post_tag
    )

    list_filter = (
        'post_date', 
        'status', 
        TopViewedFilter, 
        'journalist__registration_type', 
        'author', 
        'journalist__first_name', 
        'journalist__organisation_name', 
        'post_cat',
        'order',
        'Head_Lines',
        'articles',
        'trending',
        'BreakingNews',
        'Event',
        'post_date',
        'tags'  # ✅ Add tags here for filtering
    )

    list_display = (
        'post_title', 
        'get_posted_by', 
        'post_date',
        'slug',
        'post_status',
        'viewcounter',
        'order',
        'is_active',
        'status',
        'post_cat',
        'post_image',
        'Head_Lines',
        'articles',
        'trending',
        'BreakingNews',
        'Event',
        'Event_date',
        'schedule_date',
        'post_date',
        'updated_at',
        'get_tags' 
    )

    list_editable = ('status', 'is_active', 'order')
    cropping_fields = {'image_crop': ('post_image',)}
    readonly_fields = ('viewcounter','post_tag')
    ordering = ('-viewcounter', '-post_date')
    actions = ['export_as_csv']
    filter_horizontal = ('tags',)  # ✅ Good for many-to-many field
    prepopulated_fields = {"slug": ("meta_title",)}
    @admin.display(description='Posted By')
    def get_posted_by(self, obj):
        return obj.get_posted_by()

    @admin.display(description='Tags')
    def get_tags(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])

    class Media:
        css = {'all': ('/static/custom_style/custom_admin.css',)}

    @admin.action(description="Export selected posts as CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_posts.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Post Title', 'Post URL', 'Posted By', 'Post Date', 'Slug', 'Status',
            'View Counter', 'Order', 'Active', 'Category',
            'Image URL', 'Updated At'
        ])

        for post in queryset:
            image_url = request.build_absolute_uri(post.post_image.url) if post.post_image else ''
            post_url = request.build_absolute_uri(f"/{post.slug}")
            writer.writerow([
                post.post_title,
                post_url,
                post.get_posted_by(),
                post.post_date,
                post.slug,
                post.status,
                post.viewcounter,
                post.order,
                post.is_active,
                post.post_cat.subcat_name if post.post_cat else '',
                image_url,
                post.updated_at,
            ])

        return response

admin.site.register(NewsPost, Post_Admin)

class VideoPost(admin.ModelAdmin):
    list_display=('video_title','get_posted_by','News_Category','video_date','slug','video_url','viewcounter','counter','order','is_active','Head_Lines','articles','trending','BreakingNews','schedule_date',)
    search_fields=('video_title','News_Category__subcat_name','slug', 'author__username', 'author__first_name', 'author__last_name', 'journalist__username', 'journalist__first_name', 'journalist__last_name', 'journalist__organisation_name',)
    list_filter=('video_date','is_active', TopViewedFilter, 'journalist__registration_type', 'author', 'journalist__first_name', 'journalist__organisation_name', 'News_Category','order')
    readonly_fields = ('viewcounter',)
    list_editable=('is_active','order',)
    actions = ['export_video_posts_csv']

    class Media:
        css = { 'all': ('/static/custom_style/custom_admin.css',) }

    @admin.display(description='Posted By')
    def get_posted_by(self, obj):
        return obj.get_posted_by()
    
    @admin.action(description="Export selected video posts as CSV")
    def export_video_posts_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="video_posts.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Video Title', 'Post URL', 'Posted By', 'video_thumbnail', 'video_type', 'News Category', 'Video Date',
            'Slug', 'Video Link', 'Views', 'Counter', 'Order',
            'Active', 'Headlines', 'Articles', 'Trending',
            'Breaking News', 'Schedule Date'
        ])

        for post in queryset:
            post_url = request.build_absolute_uri(f"/video/{post.slug}")
            video_thumbnail = request.build_absolute_uri(post.video_thumbnail.url) if post.video_thumbnail else ''

            if post.video_type == 'video':
                video_link = f"https://www.youtube.com/watch?v={post.video_url}"
            elif post.video_type == 'reel':
                video_link = f"https://www.youtube.com/shorts/{post.video_url}"
            else:
                video_link = post.video_url or ''

            writer.writerow([
                post.video_title,
                post_url,
                post.get_posted_by(),
                video_thumbnail, 
                post.video_type,
                post.News_Category.subcat_name if post.News_Category else '',
                post.video_date,
                post.slug,
                video_link,
                post.viewcounter,
                post.counter,
                post.order,
                post.is_active,
                post.Head_Lines,
                post.articles,
                post.trending,
                post.BreakingNews,
                post.schedule_date,
            ])
        return response
admin.site.register(VideoNews,VideoPost)

class slideradmin(admin.ModelAdmin):
    search_fields=('title','slug')
    list_filter=('post_date','order')
    list_display=('slidercat','title','des','sliderimage','slug','post_date','updated_at','order','status',)
    list_editable=('status','order',)
    cropping_fields = {'image_crop': ('sliderimage',)}
admin.site.register(slider,slideradmin)


class cmsadmin(admin.ModelAdmin):
    search_fields=('pagename','slug')
    list_filter=('post_date','order')
    readonly_fields = ('viewcounter',)
    list_display=('pagename','Content','pageimage','slug','post_date','updated_at','viewcounter','post_status','order')
    list_editable=('post_status','order',)
    cropping_fields = {'image_crop': ('pageimage',)}
admin.site.register(CMS,cmsadmin)