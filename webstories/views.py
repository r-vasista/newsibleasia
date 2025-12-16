from django.shortcuts import render, get_object_or_404
from .models import WebStory, WebStoryCategory, WebStorySlide

def webstories_home(request):
    """Main web stories landing page with categories"""
    categories = WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    # Get featured/latest stories for each category
    category_stories = {}
    for category in categories:
        category_stories[category] = WebStory.objects.filter(
            category=category, 
            is_published=True
        ).order_by('order', '-published_date')[:10]
    
    # Get all latest stories (ordered by order field, then by date)
    latest_stories = WebStory.objects.filter(
        is_published=True
    ).order_by('order', '-published_date')[:20]
    
    context = {
        'categories': categories,
        'category_stories': category_stories,
        'latest_stories': latest_stories,
    }
    
    return render(request, 'webstories/home.html', context)


def webstories_category(request, category_slug):
    """Stories filtered by category"""
    
    # Get the specific category
    category = get_object_or_404(WebStoryCategory, slug=category_slug, is_active=True)
    
    # Get stories for this category (ordered by order field, then by date)
    stories = WebStory.objects.filter(
        category=category, 
        is_published=True
    ).order_by('order', '-published_date')
    
    # Get all categories for navigation
    categories = WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'category': category,
        'stories': stories,
        'categories': categories,
    }
    
    return render(request, 'webstories/category.html', context)


def webstory_detail(request, category_slug, story_slug):
    """Individual web story viewer"""
    category = get_object_or_404(WebStoryCategory, slug=category_slug)
    story = get_object_or_404(WebStory, slug=story_slug, category=category, is_published=True)
    
    # Increment view count
    story.views += 1
    story.save(update_fields=['views'])
    
    # Get all slides (ordered by order field)
    slides = story.slides.all().order_by('order')
    
    # Get related stories from the same category first (ordered by order, then date)
    related_stories = WebStory.objects.filter(
        category=category, 
        is_published=True
    ).exclude(id=story.id).order_by('order', '-published_date')[:4]
    
    # If not enough stories in same category, get from other categories
    if related_stories.count() < 4:
        remaining_count = 4 - related_stories.count()
        other_stories = WebStory.objects.filter(
            is_published=True
        ).exclude(
            id=story.id
        ).exclude(
            id__in=[s.id for s in related_stories]
        ).order_by('order', '-published_date')[:remaining_count]
        
        # Combine both querysets
        related_stories = list(related_stories) + list(other_stories)
    
    context = {
        'story': story,
        'slides': slides,
        'category': category,
        'related_stories': related_stories,
        'categories': WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name'),
    }
    
    return render(request, 'webstories/story_detail.html', context)


def webstories_latest(request):
    """Latest web stories page - all stories without category grouping"""
    
    # Get all latest stories (ordered by order field, then by date)
    latest_stories = WebStory.objects.filter(
        is_published=True
    ).order_by('order', '-published_date')
    
    # Get all categories for navigation
    categories = WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'latest_stories': latest_stories,
        'categories': categories,
    }
    
    return render(request, 'webstories/latest.html', context)