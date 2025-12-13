from django.urls import path
from . import views

app_name = 'webstories'

urlpatterns = [
    path('', views.webstories_home, name='home'),
    path('<slug:category_slug>/', views.webstories_category, name='category'),
    path('<slug:category_slug>/<slug:story_slug>/', views.webstory_detail, name='detail'),
]