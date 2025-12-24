from django.urls import path
from . import views

app_name = 'webstories'

urlpatterns = [
    # Home page
    path('', views.webstories_home, name='home'),
    
    # Latest stories
    path('latest/', views.webstories_latest, name='latest'),
    
    # Category page
    path('category/<slug:category_slug>/', views.webstories_category, name='category'),
    
    # Individual story (CLEAN URL - no category, no date, no ID)
    # Format: /web-stories/story-slug/
    path('<slug:story_slug>/', views.webstory_detail, name='detail'),
    
    # Bookend JSON endpoint for related stories
    path('api/bookend/<slug:story_slug>/', views.webstory_bookend_json, name='bookend_json'),
]