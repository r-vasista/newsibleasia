"""
URL configuration for newsibleasia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from newsibleasia import views
from django.conf import settings
from django.conf.urls.static import static
#from newsibleasia.sitemap import BlogSitemap,StaticSitemap
#from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

#sitmap start
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from newsibleasia.sitemaps import custom_sitemap_index, sitemap_news, sitemap_images, sitemap_images_by_month, sitemap_videos, sitemap_videos_by_month, sitemap_article, sitemap_article_by_month, sitemap_archive, sitemap_archive_by_month, sitemap_tags, sitemap_tag_detail, sitemap_static, sitemap_categories, sitemap_category_detail
#sitmap end

admin.site.site_header="newsibleasia Admin"
admin.site.site_title="newsibleasia Admin"
admin.site.index_title="Dasboard"

# sitemaps={
#      'post':BlogSitemap,
#      'StaticUrl':StaticSitemap
#    }

urlpatterns = [
    path('', views.home, name="home"),
    path('auth/', include('journalist.urls')),
    path('topic/<slug:slug>', views.posts_by_tag, name='posts_by_tag'),
    path('artdomain/<str:username>/', views.profiledxb, name='journalist_profile'),
    path("send-otp/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('thanks', views.thanks, name="thanks"),
    path('error', views.ErrorPage, name="error"),
    path('contact-us', views.Contactus, name="contact-us"),
    path('sitemap-page', views.SiteMap, name="sitemap-page"),
    path('advertise-with-us', views.advertise, name="advertise-with-us"),
    path('upcoming-events', views.UcEvents, name="upcoming-events"),
    path('news-pdf', views.GetNewsPdf, name="news-pdf"),
    path('career', views.Career, name="career"),
    path('UserSubscriber', views.SubscribeView, name="UserSubscriber"),
    path('Reg-Form', views.Reg_Form, name="Reg-Form"),
    path('search', views.find_post_by_title, name="search"),
    path('adsinquiry', views.Adsinquiry, name='adsinquiry'),
    path('voices-of-uae', views.Adsinquiry, name='voices-of-uae'),
    #recon path
    path('newsibileasia/api/', include('portal.urls')),
    
    #path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    # path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path(
        "ads.txt",
        TemplateView.as_view(template_name="ads.txt", content_type="text/plain"),
    ),
    
    #sitmap start
    path('sitemap', custom_sitemap_index, name='sitemap'),
    path('sitemap/news', sitemap_news, name='sitemap-news'),
    path('sitemap/images', sitemap_images, name='sitemap-images'),
    path('sitemap/images/<int:year>/<int:month>/', sitemap_images_by_month, name='sitemap-images-by-month'),
    path('sitemap/videos', sitemap_videos, name='sitemap-video'),
    path('sitemap/videos/<int:year>/<int:month>/', sitemap_videos_by_month, name='sitemap-videos-by-month'),
    path('sitemap/articles', sitemap_article, name='sitemap-articles'),
    path('sitemap/articles/<int:year>/<int:month>/', sitemap_article_by_month, name='sitemap-articles-by-month'),
    path('sitemap/archive', sitemap_archive, name='sitemap-archive'),
    path('sitemap/archive/<int:year>/<int:month>/', sitemap_archive_by_month, name='sitemap-archive-by-month'),
    #new tag sitemap
    
    path('sitemap/tags', sitemap_tags, name='sitemap-tags'),
    path('sitemap/tags/<slug:slug>', sitemap_tag_detail, name='sitemap-tag-detail'),
    path('sitemap/static', sitemap_static, name='sitemap-static'),
    path('sitemap/categories', sitemap_categories, name='sitemap-categories'),
    path('sitemap/categories/<slug:slug>', sitemap_category_detail, name='sitemap-category-detail'),
    #sitmap end
    #admin-user-pannel-path
    path('user-dashboard', views.Userdashboard, name="user-dashboard"),
    path('managepost', views.ManagePost, name="managepost"),
    path('guest-news-post', views.Guestpost, name="guest-news-post"),
    path('registration', views.Userregistration, name="registration"),
    path('registeration', views.Registeration, name="registeration"),
    path('login', views.Userlogin, name="login"),
    path('logout', views.Logout, name="logout"),
    path('edit-news-post/<int:post_id>', views.EditNewsPost, name="edit-news-post"),
    path('update-post', views.UpdateNewsPost, name="update-post"),
    
    #dynemic-path---
    path('<slug>', views.newsdetails, name="newsdetails"),
    path('all-news/<slug>', views.AllNews, name="all-news"),
    path('all-video-news/<slug>', views.AllvideoNews, name="all-video-news"),
    path('video/<slug>', views.videonewsdetails, name="videonewsdetails"),
    path('<str:catlink>/<slug>', views.catdetails, name="catdetails"),
    path('events/<slug>', views.eventdetails, name="eventdetails"),
    #dynemic-path-end
    
    #path('logincheck', views.Logincheck, name="logincheck"),
    #admin-----link---end------

    #path('video/<slug>', views.videocategory, name="videocategory"),
    # path('<data>', views.pagename),
    
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('<slug:slug>/', views.cms_detail, name='cms'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
