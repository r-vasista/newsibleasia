from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import WebStory, WebStoryCategory, WebStorySlide

def webstories_home(request):
    """Main web stories landing page with categories"""
    categories = WebStoryCategory.objects.filter(is_active=True)
    
    # Get featured/latest stories for each category
    category_stories = {}
    for category in categories:
        category_stories[category] = WebStory.objects.filter(
            category=category, 
            is_published=True
        )[:10]
    
    # Get all latest stories
    latest_stories = WebStory.objects.filter(is_published=True)[:20]
    
    context = {
        'categories': categories,
        'category_stories': category_stories,
        'latest_stories': latest_stories,
    }
    
    return render(request, 'webstories/home.html', context)


def webstories_category(request, category_slug):
    """Stories filtered by category"""
    category = get_object_or_404(WebStoryCategory, slug=category_slug, is_active=True)
    stories = WebStory.objects.filter(category=category, is_published=True)
    print(stories)
    
    context = {
        'category': category,
        'stories': stories,
        'categories': WebStoryCategory.objects.filter(is_active=True),
    }
    
    return render(request, 'webstories/category.html', context)


def webstory_detail(request, category_slug, story_slug):
    """Individual web story viewer"""
    category = get_object_or_404(WebStoryCategory, slug=category_slug)
    story = get_object_or_404(WebStory, slug=story_slug, category=category, is_published=True)
    
    # Increment view count
    story.views += 1
    story.save(update_fields=['views'])
    
    # Get all slides
    slides = story.slides.all()
    
    # Get related stories
    related_stories = WebStory.objects.filter(
        category=category, 
        is_published=True
    ).exclude(id=story.id)[:6]
    
    context = {
        'story': story,
        'slides': slides,
        'category': category,
        'related_stories': related_stories,
        'categories': WebStoryCategory.objects.filter(is_active=True),
    }
    
    return render(request, 'webstories/story_detail.html', context)