from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import WebStory, WebStoryCategory, WebStoryPage

def webstories_home(request):
    """Main web stories landing page"""
    categories = WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    # Get stories for each category
    category_stories = {}
    for category in categories:
        category_stories[category] = WebStory.objects.filter(
            category=category, 
            is_published=True
        ).order_by('order', '-published_date')[:10]
    
    # Get latest stories
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
    category = get_object_or_404(WebStoryCategory, slug=category_slug, is_active=True)
    
    stories = WebStory.objects.filter(
        category=category, 
        is_published=True
    ).order_by('order', '-published_date')
    
    categories = WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'category': category,
        'stories': stories,
        'categories': categories,
    }
    
    return render(request, 'webstories/category.html', context)


def webstory_detail(request, story_slug):
    """
    Individual AMP Web Story
    URL: /web-stories/story-slug/ (clean URL as per guidelines)
    """
    story = get_object_or_404(
        WebStory, 
        slug=story_slug, 
        is_published=True
    )
    
    # Increment view count
    story.views += 1
    story.save(update_fields=['views'])
    
    # Get all pages ordered
    pages = story.pages.all().order_by('order')
    
    # Check if story has minimum pages
    if pages.count() < 5:
        # Redirect to admin or show error
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.warning(request, 'This story needs at least 5 pages.')
        return redirect('webstories:home')
    
    context = {
        'story': story,
        'pages': pages,
    }
    
    return render(request, 'webstories/amp_story.html', context)


def webstories_latest(request):
    """Latest web stories page"""
    latest_stories = WebStory.objects.filter(
        is_published=True
    ).order_by('order', '-published_date')
    
    categories = WebStoryCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'latest_stories': latest_stories,
        'categories': categories,
    }
    
    return render(request, 'webstories/latest.html', context)


def webstory_bookend_json(request, story_slug):
    """
    AMP Bookend JSON endpoint
    Provides related stories for the bookend (shows after last page)
    """
    story = get_object_or_404(WebStory, slug=story_slug, is_published=True)
    
    # Get related stories from same category first
    related_stories = WebStory.objects.filter(
        category=story.category, 
        is_published=True
    ).exclude(id=story.id).order_by('order', '-published_date')[:4]
    
    # If not enough, get from other categories
    if related_stories.count() < 4:
        remaining = 4 - related_stories.count()
        other_stories = WebStory.objects.filter(
            is_published=True
        ).exclude(id=story.id).exclude(
            id__in=[s.id for s in related_stories]
        ).order_by('order', '-published_date')[:remaining]
        
        related_stories = list(related_stories) + list(other_stories)
    
    # Build bookend JSON (AMP format)
    bookend_data = {
        "bookendVersion": "v1.0",
        "shareProviders": [
            {
                "provider": "facebook",
            },
            {
                "provider": "twitter"
            },
            {
                "provider": "whatsapp"
            },
            {
                "provider": "email"
            },
            {
                "provider": "system"
            }
        ],
        "components": [
            {
                "type": "heading",
                "text": "More Stories For You"
            },
            {
                "type": "small",
                "title": "Explore more trending stories",
                "url": request.build_absolute_uri('/webstories/'),
                "image": request.build_absolute_uri('/static/images/logo.png') if hasattr(request, 'build_absolute_uri') else ""
            }
        ]
    }
    
    # Add related stories as landscape cards
    for related in related_stories:
        bookend_data["components"].append({
            "type": "landscape",
            "title": related.title,
            "url": request.build_absolute_uri(related.get_absolute_url()),
            "image": request.build_absolute_uri(related.poster_portrait.url),
            "category": related.category.name
        })
    
    # Add "View All Stories" button at the end
    bookend_data["components"].append({
        "type": "cta-link",
        "links": [
            {
                "text": "View All Stories",
                "url": request.build_absolute_uri('/webstories/')
            }
        ]
    })
    
    return JsonResponse(bookend_data)
