import logging

logger = logging.getLogger(__name__)

from django.http import HttpResponse

from django.db.models import Q

from post_management.models import category,sub_category,NewsPost,VideoNews,Tag, NewsRedirect

from setting.models import profile_setting, CMS

from Ad_management.models import ad_category

from Ad_management.models import ad

from Seo_management.models import seo_optimization

from service.models import jobApplication, CareerApplication, SubscribeUser, BrandPartner, RegForm, AdsEnquiry



from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import login, logout, authenticate

from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

#from store.models import Product

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse, Http404

from datetime import date, datetime

import re

from django.utils import timezone

import random

from django.core.cache import cache

from django.views.decorators.csrf import csrf_exempt

from itertools import islice

from journalist.models import Journalist

from django.core.exceptions import ObjectDoesNotExist


from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django_user_agents.utils import get_user_agent

# home-pahe---------

def home(request):

    seo=seo_optimization.objects.get(pageslug='https://www.newsibleasia.com')

    current_datetime = datetime.now()

    blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-id')[:10]

    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]

    events=NewsPost.objects.filter(schedule_date__lt=current_datetime,Event=1,status='active').order_by('-id')[:10]

    bp=BrandPartner.objects.filter(is_active=1).order_by('-id')[:30]

    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id')[:12]

    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id')[:8]

    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id')[:6]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id')[:4]

    user_news = NewsPost.objects.filter(schedule_date__lt=current_datetime, journalist_id__isnull=False, status='active').order_by('-id')[:10]

    profiles = Journalist.objects.filter(status='active').exclude(registration_type='journalist').order_by('-id')[:6]

    Category = category.objects.filter(cat_status='active').order_by('order')[:12]

    grouped_postsdata = {}



    for cat in Category:

        subcategories = cat.sub_category_set.all()

        category_posts = NewsPost.objects.filter(Q(post_cat__in=subcategories), is_active=1, status='active', schedule_date__lte=timezone.now()).order_by('-schedule_date')[:10]



        grouped_postsdata[cat] = {"subcategories": subcategories, "posts": category_posts,}



    grouped_postsdata_items = list(grouped_postsdata.items())

    grouped_postsdata1 = dict(grouped_postsdata_items[:2])

    grouped_postsdata2 = dict(grouped_postsdata_items[2:])

    

    truet=VideoNews.objects.filter(is_active='active',video_type='reel',News_Category=75).order_by('-id')[:8]

    recipe=VideoNews.objects.filter(is_active='active',video_type='reel',News_Category=76).order_by('-id')[:8]

# --------------video-post-manage--------------

    podcast=VideoNews.objects.filter(is_active='active',video_type='video',Head_Lines=1).order_by('order')[:2]

    mainvid=VideoNews.objects.filter(is_active='active',video_type='video',order__range=[3, 6]).order_by('order')[:4]

    video=VideoNews.objects.filter(is_active='active',video_type='video').order_by('order')[:5]

    reel=VideoNews.objects.filter(is_active='active',video_type='reel').order_by('-id')[:16]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:3]

# --------------ad-manage-meny--------------

    lfsid=ad_category.objects.get(ads_cat_slug='left-fest-square')

    leftsquqre=ad.objects.filter(ads_cat_id=lfsid.id, is_active=1).order_by('-id') [:4]

    

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    # header--to--ad---

    topad=ad_category.objects.get(ads_cat_slug='topad')

    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]

    

    popup=ad_category.objects.get(ads_cat_slug='popup')

    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]

# -------------end-ad-manage-meny--------------    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'indseo':seo,

            'LatestNews':blogdata,

            'mainnews':mainnews,

            'events':events,

            'bplogo':bp,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'headtopad':tophead,

            'popup':popupad,

            'lfs':leftsquqre,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

            'MainV':mainvid,

            'videos':video,

            'Reels':reel,

            'recipe':recipe,

            'tt':truet,

            'grouped_postsdata': grouped_postsdata1,

            'grouped_postsdata2': grouped_postsdata2,

            'usernews': user_news,

            'profiles': profiles,
            

        }

    return render(request,'index.html',data)

# News-details-page----------



def newsdetails(request, slug):
    try:
        current_datetime = datetime.now()

        counter = NewsPost.objects.get(slug=slug)
        counter.viewcounter = counter.viewcounter + 1
        counter.save()

        seo = 'ndetail'

        blogdetails = NewsPost.objects.get(slug=slug, status='active')

        blogdata = NewsPost.objects.filter(
            schedule_date__lt=current_datetime,
            is_active=1,
            status='active'
        ).order_by('-id')[:9]

        mainnews = NewsPost.objects.filter(
            schedule_date__lt=current_datetime,
            is_active=1,
            status='active'
        ).order_by('-id')[:2]

        articales = NewsPost.objects.filter(
            schedule_date__lt=current_datetime,
            articles=1,
            status='active'
        ).order_by('-id')[:3]

        headline = NewsPost.objects.filter(
            schedule_date__lt=current_datetime,
            Head_Lines=1,
            status='active'
        ).order_by('-id')[:4]

        trending = NewsPost.objects.filter(
            schedule_date__lt=current_datetime,
            trending=1,
            status='active'
        ).order_by('-id')[:8]

        brknews = NewsPost.objects.filter(
            schedule_date__lt=current_datetime,
            BreakingNews=1,
            status='active'
        ).order_by('-id')[:8]

        podcast = VideoNews.objects.filter(
            is_active='active'
        ).order_by('-id')[:1]

        vidarticales = VideoNews.objects.filter(
            articles=1,
            is_active='active',
            video_type='video'
        ).order_by('order')[:2]

        # Ad Sections
        lfsid = ad_category.objects.get(ads_cat_slug='left-fest-square')
        leftsquqre = ad.objects.filter(
            ads_cat_id=lfsid.id, is_active=1
        ).order_by('-id')[:4]

        adtlid = ad_category.objects.get(ads_cat_slug='topleft-600x80')
        adtopleft = ad.objects.filter(
            ads_cat_id=adtlid.id, is_active=1
        ).order_by('-id')[:1]

        adtrid = ad_category.objects.get(ads_cat_slug='topright-600x80')
        adtopright = ad.objects.filter(
            ads_cat_id=adtrid.id, is_active=1
        ).order_by('-id')[:1]

        adtopid = ad_category.objects.get(ads_cat_slug='leaderboard')
        adtop = ad.objects.filter(
            ads_cat_id=adtopid.id, is_active=1
        ).order_by('-id')[:1]

        adleftid = ad_category.objects.get(ads_cat_slug='skyscraper')
        adleft = ad.objects.filter(
            ads_cat_id=adleftid.id, is_active=1
        ).order_by('-id')[:1]

        adrcol = ad_category.objects.get(ads_cat_slug='mrec')
        adright = ad.objects.filter(
            ads_cat_id=adrcol.id, is_active=1
        ).order_by('-id')[:1]

        festbg = ad_category.objects.get(ads_cat_slug='festivebg')
        festive = ad.objects.filter(
            ads_cat_id=festbg.id, is_active=1
        ).order_by('-id')[:1]

        Category = category.objects.filter(
            cat_status='active'
        ).order_by('order')[:12]

        slider = NewsPost.objects.order_by('-id')[:5]
        latestnews = NewsPost.objects.order_by('-id')[:5]

        data = {
            'indseo': seo,
            'Blogdetails': blogdetails,
            'BlogData': blogdata,
            'mainnews': mainnews,
            'Slider': slider,
            'Blogcat': Category,
            'latnews': latestnews,
            'adtop': adtop,
            'adleft': adleft,
            'adright': adright,
            'adtl': adtopleft,
            'adtr': adtopright,
            'bgad': festive,
            'lfs': leftsquqre,
            'Articale': articales,
            'vidart': vidarticales,
            'headline': headline,
            'trendpost': trending,
            'bnews': brknews,
            'vidnews': podcast,
        }

        return render(request, 'news-details.html', data)

    except ObjectDoesNotExist:
        # Check if there's a redirect for this slug
        try:
            news_redirect = NewsRedirect.objects.get(old_slug=slug, is_active=True)
            # Perform a 301 permanent redirect (best for SEO)
            return redirect('newsdetails', slug=news_redirect.redirect_slug, permanent=True)
        except NewsRedirect.DoesNotExist:
            # No redirect found, show 404
            raise Http404("News post not found")
    except Exception as e:
        print('error',str(e))
        raise Http404("News post not found")

# News-pdf--------

def GetNewsPdf(request):

    current_datetime = datetime.now()

    blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-id') [:10]

    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]

    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]

    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:4]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:3]

    data={

            # 'indseo':seo,

            'BlogData':blogdata,

            'mainnews':mainnews,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            

        }

    return render(request,'epaper.html',data)



# News-pdf--------

# News-News-search--------

def find_post_by_title(request):

    seo='allnews'

    current_datetime = datetime.now()

    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]

    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]

    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

    topad=ad_category.objects.get(ads_cat_slug='topad')

    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]

    popup=ad_category.objects.get(ads_cat_slug='popup')

    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]

# -------------end-ad-manage-meny--------------    



    title = request.GET.get('title')

    if title:

        blogdata = NewsPost.objects.filter(post_title__contains=title,is_active=1,status='active')

        if blogdata.exists():

            data={

                'indseo':seo,

                'BlogData':blogdata,

                'event':events,

                'bplogo':bp,

                'Blogcat':Category,

                'adtop':adtop,

                'adleft':adleft,

                'adright':adright,

                'adtl':adtopleft,

                'adtr':adtopright,

                'bgad':festive,

                'headtopad':tophead,

                'popup':popupad,

                'Articale':articales,

                'vidart':vidarticales,

                'headline':headline,

                'bnews':brknews,

                'vidnews':podcast,

                'trendpost':trending,

                }

            return render(request, 'all-news.html', data)

        else:

            data={

                'messages':'No Data Found!',

                }

            return render(request, 'error.html', data)

    else:

        data={

            'messages':'No Data Found!',

            }

        return render(request, 'error.html', data)

# News-News-search-end-------



# error-page-------

def ErrorPage(request):

    data={

        'messages':'No Data Found!',

        }

    return render(request, 'thanks.html', data)

# error-page-------





# All-News-----------

def AllNews(request,slug):

    alnslug='/all-news/'+ slug

    seo=seo_optimization.objects.get(pageslug=alnslug)

    current_datetime = datetime.now()

    page_number = request.GET.get('page', 1)  

    # Get the page number from the request, default to 1 if not provided

    if slug == 'articles':

        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-schedule_date')

        podcast=VideoNews.objects.filter(is_active='active',articles=1).order_by('-schedule_date') [:3]

    elif slug == 'breaking':

        blogdata=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-schedule_date') [:100]

        podcast=VideoNews.objects.filter(is_active='active',BreakingNews=1).order_by('-schedule_date') [:3]

    elif slug == 'head-lines':

        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-schedule_date') [:100]

        podcast=VideoNews.objects.filter(is_active='active',Head_Lines=1).order_by('-schedule_date') [:3]

    elif slug == 'trending':

        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-schedule_date') [:100]

        podcast=VideoNews.objects.filter(is_active='active',trending=1).order_by('-schedule_date') [:3]

    elif slug == 'latest':

        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-schedule_date') [:1000]

        podcast=VideoNews.objects.filter(is_active='active',).order_by('-schedule_date') [:3]

    else:

        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-schedule_date') [:200]

        podcast=VideoNews.objects.filter(is_active='active').order_by('-schedule_date') [:3]

    

    paginator = Paginator(blogdata, 12)   



    try:

        blogdata = paginator.page(page_number)

    except PageNotAnInteger:

        # If page is not an integer, deliver first page.

        blogdata = paginator.page(1)

    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.

        blogdata = paginator.page(paginator.num_pages) 

        

    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]

    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]

    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]

    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-schedule_date') [:12]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-schedule_date') [:14]

    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-schedule_date') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-schedule_date') [:8]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

# --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

    topad=ad_category.objects.get(ads_cat_slug='topad')

    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]

    popup=ad_category.objects.get(ads_cat_slug='popup')

    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]

# -------------end-ad-manage-meny--------------    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'indseo':seo,

            'BlogData':blogdata,

            'mainnews':mainnews,

            'event':events,

            'bplogo':bp,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'headtopad':tophead,

            'popup':popupad,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

        }

   

    return render(request,'all-news.html',data)

    #return render(request, 'index.html')

# News-details-page--end--------





# Video-all-News-details-----------

def AllvideoNews(request,slug):

    alnslug='/all-video-news/'+ slug

    seo=seo_optimization.objects.get(pageslug=alnslug)

    

    if slug == 'articles':

        blogdata=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('-id')

    elif slug == 'breaking':

        blogdata=VideoNews.objects.filter(BreakingNews=1,is_active='active',video_type='video').order_by('-id') [:100]

    elif slug == 'head-lines':

        blogdata=VideoNews.objects.filter(Head_Lines=1,is_active='active',video_type='video').order_by('-id') [:100]

    elif slug == 'trending':

        blogdata=VideoNews.objects.filter(trending=1,is_active='active',video_type='video').order_by('-id') [:100]

    elif slug == 'stories':

        blogdata=VideoNews.objects.filter(is_active='active',video_type='reel').order_by('-id')

    else:

        blogdata=VideoNews.objects.filter(is_active='active',video_type='video').order_by('-id')

        

    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]

    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

# --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

    topad=ad_category.objects.get(ads_cat_slug='topad')

    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]

    popup=ad_category.objects.get(ads_cat_slug='popup')

    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]

# -------------end-ad-manage-meny--------------    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'indseo':seo,

            'BlogData':blogdata,

            'mainnews':mainnews,

            'event':events,

            'bplogo':bp,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'headtopad':tophead,

            'popup':popupad,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

        }

   

    return render(request,'all-video-news.html',data)

    #return render(request, 'index.html')

# Video-all-News-details-page--end--------





# Events-page----------

def UcEvents(request):

    seo='Event'

    eventdata=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:100]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

# --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

    topad=ad_category.objects.get(ads_cat_slug='topad')

    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]

    popup=ad_category.objects.get(ads_cat_slug='popup')

    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]

# -------------end-ad-manage-meny--------------    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'indseo':seo,

            'EventData':eventdata,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'headtopad':tophead,

            'popup':popupad,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

        }

   

    return render(request,'upcoming-events.html',data)

    #return render(request, 'index.html')

# Events-page--end--------

def eventdetails(request,slug):

    seo='eventdetails'

    subcatid=sub_category.objects.get(subcat_slug=slug)

    

    catvid=VideoNews.objects.filter(News_Category=subcatid.id,is_active='active',video_type='video').order_by('order')[:50]

    if not catvid:

        catvid="no data"

    #using regex post_tag__regex for search  match....

    databytag=NewsPost.objects.filter(status='active').filter(post_tag__regex = rf'^(\D+){subcatid.subcat_tag}(\D+)').order_by('-id') [:400]

    

    blogdata=NewsPost.objects.filter(is_active=1,status='active',post_cat=subcatid.id).order_by('-id') [:20]

    eventdata=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:100]

    

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

        

    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]

    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

# --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

    topad=ad_category.objects.get(ads_cat_slug='topad')

    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]

    popup=ad_category.objects.get(ads_cat_slug='popup')

    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]

# -------------end-ad-manage-meny--------------    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'indseo':seo,

            'BlogData':blogdata,

            'mainnews':mainnews,

            'event':events,

            'bplogo':bp,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'headtopad':tophead,

            'popup':popupad,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

            'CatV':catvid,

            'subcat':subcatid,

            'evedata':eventdata,

            'bytag':databytag

        }

    return render(request,'eventdetails.html',data)



# News-details-page----------

def videonewsdetails(request,slug):

    counter=VideoNews.objects.get(slug=slug)

    counter.viewcounter=counter.viewcounter + 1

    counter.save()

    seo='video'

    current_datetime = datetime.now()

    viddetails=VideoNews.objects.get(slug=slug)

    blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-id') [:20]

    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]

    

    vidarticales=VideoNews.objects.filter(schedule_date__lt=current_datetime,is_active='active',video_type='video').order_by('order')[:9]

    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id') [:4]

    brknews=NewsPost.objects.filter(schedule_date__lt=current_datetime,BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(schedule_date__lt=current_datetime,is_active='active').order_by('-id') [:1]

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

    # festivetop

    # festiveleft

    # festiveright

# -------------end-ad-manage-meny--------------    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'indseo':seo,

            'Vnews':viddetails,

            'BlogData':blogdata,

            'mainnews':mainnews,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

        }

    return render(request,'video-news-details.html',data)

    #return render(request, 'index.html')

# News-details-page--end--------





# cat-details-page---------

def catdetails(request,catlink,slug):

    current_datetime = datetime.now()

    seourl='/'+catlink+'/'+slug

    seoslug = seourl.replace("-", " ").upper()

   

    try:

        seo = seo_optimization.objects.get(pageslug=seourl)

    except seo_optimization.DoesNotExist:

        seo=seo_optimization.objects.get(pageslug='https://www.newsibleasia.com/')



    subcatid = sub_category.objects.get(subcat_slug=slug)



    Latest_News = NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime,is_active=1, status='active').order_by('-id')[:3]

    blogdata_list = NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime, status='active').order_by('-id')

    headline = NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime, Head_Lines=1, status='active').order_by('-id')

    articales = NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime, articles=1, status='active').order_by('-id')

    trending = NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime, trending=1, status='active').order_by('-id')

    brknews = NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime, BreakingNews=1, status='active').order_by('-id')

    videos = VideoNews.objects.filter(schedule_date__lt=current_datetime, is_active='active', video_type='video').order_by('order')

    reels = VideoNews.objects.filter(News_Category=subcatid.id,schedule_date__lt=current_datetime, is_active='active', video_type='reel').order_by('order')

    podcast = VideoNews.objects.filter(News_Category=subcatid.id,schedule_date__lt=current_datetime, is_active='active').order_by('order')



    blogdata = Paginator(blogdata_list, 12).get_page(request.GET.get('page'))

    headline_page = Paginator(headline, 5).get_page(request.GET.get('headline_page'))

    articles_page = Paginator(articales, 5).get_page(request.GET.get('articles_page'))

    trending_page = Paginator(trending, 7).get_page(request.GET.get('trending_page'))

    brknews_page = Paginator(brknews, 8).get_page(request.GET.get('brknews_page'))

    videos_page = Paginator(videos, 10).get_page(request.GET.get('videos_page'))

    reels_page = Paginator(reels, 10).get_page(request.GET.get('reels_page'))

    podcast_page = Paginator(podcast, 7).get_page(request.GET.get('podcast_page'))



    for video in videos_page:

        video.get_absolute_url = lambda slug=video.slug: f"/video/{slug}"





    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    

# -------------end-ad-manage-meny--------------   

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={ 

            'indseo':seo,

            'sslug':seoslug,

            'slugurl':catlink+'/'+slug,

            'latestnews':Latest_News,

            'BlogData':blogdata,

            'headline': headline_page,

            'Articale': articles_page,

            'trendpost': trending_page,

            'breakingnews': brknews_page,

            'videos': videos_page,

            'reels': reels_page,

            'vidnews': podcast_page,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

        }



    return render(request,'category.html',data)

# cat-details-page--end--------




from service.models import Contact
# cat-contact-page---------
def Contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact.save()
        messages.success(request, 'Your message has been submitted successfully.')
        return redirect('contact-us') 


    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
    Category=category.objects.filter(cat_status='active').order_by('order') [:12]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------   
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
    return render(request,'contact.html',data)
# cat-contact-page--end--------
# cat-contact-page--end--------



# cat-registration-page---------

def Userregistration(request):

    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]

    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    festbg=ad_category.objects.get(ads_cat_slug='festivebg')

    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    # festivetop

    # festiveleft

    # festiveright

# -------------end-ad-manage-meny--------------   

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'mainnews':mainnews,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'bgad':festive,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

        }

    return render(request,'inn/registrations.html',data)



def Registeration(request):

    if request.method == "POST":

        fname=request.POST.get('fname')

        lname=request.POST.get('lname')

        username=request.POST.get('username')

        email=request.POST.get('email')

        #contact=request.POST.get('contact')

        if request.POST.get('password1')==request.POST.get('password2'):

            password=request.POST.get('password1')

            user=User(

                first_name=fname,

                last_name=lname,

                username = username,

                email = email,

                )

            user.set_password(password)

            user.save()

            if user is not None:

                messages.success(request, 'You Are Registered successfully!')

                return redirect(Userlogin)

            else:

                messages.success(request, 'You Are Not Registered !')

        else:

            messages.success(request, 'The password dose not match !')

    return render(request,'registration.html')

        #messages.success(request, 'Your message was successfully sent!')

    

# cat-registration-page--end--------



# start-subscriber-page-----------





def SubscribeView(request):

    if request.method == "POST":

        fname = request.POST.get('fname')

        email = request.POST.get('email')



        if not fname or not email:

            return JsonResponse({"status": "error", "message": "Name and Email are required."})



        if SubscribeUser.objects.filter(email=email).exists():

            return JsonResponse({"status": "error", "message": "You have already subscribed!"})



        try:

            ip = request.META.get('REMOTE_ADDR', '')

            country = request.META.get('GEOIP_COUNTRY_NAME', '')

            city = request.META.get('GEOIP_CITY', '')



            SubUser = SubscribeUser(

                name=fname,

                email=email,

                ip=ip,

                country=country,

                city=city,

            )

            SubUser.save()



            message = f"""

            Subject: Welcome to DXB News Network - Your Source for Insightful News!

            Dear {fname},

            Thank you for subscribing to DXB News Network! Stay updated with the latest news.

                Regards,

                DXB News Network

            """

            send_mail(

                "Welcome to DXB News Network",

                message,

                "no-reply@newsibleasia.com",

                [email],

                fail_silently=False,

            )

            return JsonResponse({"status": "success", "message": "You are registered successfully!"})



        except Exception as e:

            return JsonResponse({"status": "error", "message": "An error occurred while saving your data."})

    return render(request, 'index.html')



@csrf_exempt

def send_otp(request):

    if request.method == "POST":

        email = request.POST.get("email")

        otp = random.randint(100000, 999999)

        cache.set(f"otp_{email}", otp, timeout=300)



        otp_from_cache = cache.get(f"otp_{email}")



        send_mail(

            "Your Secure OTP for DXB News Network",

            f"Hello,\n\nYour OTP is: {otp_from_cache}.\n\nPlease use this code within 5 minutes. If you didn't request this, please ignore this email.\n\nThank you,\nDXB News Network Team",

            "no-reply@newsibleasia.com",

            [email],

            fail_silently=False,

        )



        return JsonResponse({"status": "success", "message": "OTP sent successfully!"})



    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@csrf_exempt

def verify_otp(request):

    if request.method == "POST":

        email = request.POST.get("email")

        entered_otp = request.POST.get("otp")



        stored_otp = cache.get(f"otp_{email}")



        if stored_otp and str(stored_otp) == entered_otp:

            return JsonResponse({"status": "success", "message": "OTP verified successfully!"})

        else:

            return JsonResponse({"status": "error", "message": "Invalid or expired OTP"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# subscribe-page--end--------





def Reg_Form(request):

    if request.method == "POST":

            pname=request.POST.get('person_name')

            cname=request.POST.get('company_name')

            cadd=request.POST.get('company_address')

            phone=request.POST.get('phone')

            email=request.POST.get('email')

            city=request.POST.get('city')

            country=request.POST.get('country')

            dgn=request.POST.get('designation')

            et=request.POST.get('enquiry_type')

            staff=request.POST.get('executive_names')

            sf=request.POST.get('source_from')

            win=request.POST.get('walk_in')

            ip=request.META['REMOTE_ADDR']

            

            RegUser=RegForm(

                person_name=pname,

                company_name=cname,

                company_address= cadd,

                phone=phone,

                email=email,

                city= city,

                country=country,

                diesgantion=dgn,

                enquiry_type=et,

                executive_names=staff,

                source_from=sf,

                walk_in=win,

                ip=ip

                )

            RegUser.save()

            if RegUser is not None:

                messages.success(request, 'You Are Registered successfully!')

                return redirect(thanks)

            else:

                messages.success(request, 'You Are Not Registered !')

        

    return render(request,'thanks.html')

        #messages.success(request, 'Your message was successfully sent!')

    

# cat-subscribe-page--end--------



# cat-Userlogin-page---------

def Userlogin(request):

    seo=seo_optimization.objects.get(pageslug='/login')

    if request.method == "POST":

        uname=request.POST.get('username')

        password=request.POST.get('password')

        user = authenticate(username=uname, password=password)

        if user is not None:

            login(request,user)

            return redirect(Userdashboard)

        else:

            messages.success(request, 'User and Password Wrong!')

            

        return render(request,'login.html')

      

    else:    

        blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]

        mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

        articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

        vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

        headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

        trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]

        brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

        podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]

        Category=category.objects.filter(cat_status='active').order_by('order') [:12]



        # --------------ad-manage-meny--------------

        adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

        adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

        

        adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

        adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

        

        adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

        adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

        

        adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

        adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

        

        adrcol=ad_category.objects.get(ads_cat_slug='mrec')

        adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

        festbg=ad_category.objects.get(ads_cat_slug='festivebg')

        festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]

    # festivetop

    # festiveleft

    # festiveright

    # -------------end-ad-manage-meny--------------  

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value



        slider=NewsPost.objects.filter().order_by('-id')[:5]

        latestnews=NewsPost.objects.all().order_by('-id')[:5]

        data={

                'indseo':seo,

                'BlogData':blogdata,

                'mainnews':mainnews,

                'Slider':slider,

                'Blogcat':Category,

                'latnews':latestnews,

                'adtop':adtop,

                'adleft':adleft,

                'adright':adright,

                'adtl':adtopleft,

                'adtr':adtopright,

                'bgad':festive,

                'Articale':articales,

                'vidart':vidarticales,

                'headline':headline,

                'trendpost':trending,

                'bnews':brknews,

                'vidnews':podcast,

            }

    return render(request,'inn/login.html',data)



# def Logincheck(request):

#     if request.method == "POST":

#         form = AuthenticationForm(request, data=request.POST)

#         if form.is_valid():

#             user=form.get_user()

#             login(request,user)

#             return redirect(Userdashboard)

#     else:

#         initial_data={'username':'','password':''}

#         form =AuthenticationForm(initial=initial_data)

#         #return redirect('Userlogin')

#     return render(request,'login.html',{'form':form})

# cat-Userlogin-page--end--------



# cat-Userdashboard-page---------

@login_required(login_url="/login")

def Userdashboard(request):

    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]

    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    Categories=category.objects.filter(cat_status='active').order_by('order') [:11]

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]



    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]



    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]



    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]



    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]



    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'mainnews':mainnews,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

            'categories':Categories

        }

    

    return render(request,'inn/user-dashboard.html',data)

# cat-Userdashboard-page--end--------



# cat-ManagePost-page---------

@login_required(login_url="/login")

def ManagePost(request):

    blogdata = NewsPost.objects.filter(author=request.user, is_active=1).order_by('-id')[:20]

    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    Categories=category.objects.filter(cat_status='active').order_by('order') [:11]

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]



    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]



    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]



    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]



    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]



    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'mainnews':mainnews,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'vidnews':podcast,

            'categories':Categories

        }

    

    return render(request,'inn/managepost.html',data)

# cat-ManagePost-page--end--------



# cat-logout-page---------

def Logout(request):

    logout(request)

    return redirect('login')





# cat-career-page---------

@login_required(login_url="/login")

def Career(request):

    if request.method == "POST":    

        name=request.POST.get('name')

        mobnumber=request.POST.get('mobnumber')

        email=request.POST.get('email')

        location=request.POST.get('location')

        nationality=request.POST.get('nationality')

        language=request.POST.get('language')

        address=request.POST.get('address')

        highestedu=request.POST.get('highestedu')

        fos=request.POST.get('fos')

        occupation=request.POST.get('occupation')

        journalexp=request.POST.get('journalexp')

        lastwork=request.POST.get('lastwork')

        portfolio=request.POST.get('portfolio')

        category1=request.POST.get('category')

        equipment=request.POST.get('equipment')

        softwareskill=request.POST.get('softwareskill')

        availability=request.POST.get('availability')

        resume=request.FILES.get('resume')

        whyjoin=request.POST.get('whyjoin')

        anysegment=request.POST.get('anysegment')

        career=CareerApplication(

                name=name,

                mobnumber=mobnumber,

                email=email,

                location=location,

                nationality=nationality,

                language=language,

                address=address,

                highestedu=highestedu,

                fos=fos,

                occupation=occupation,

                journalexp=journalexp,

                lastwork=lastwork,

                portfolio=portfolio,

                category=category1,

                equipment=equipment,

                softwareskill=softwareskill,

                availability=availability,

                resume=resume,

                whyjoin=whyjoin,

                anysegment=anysegment,

                )

        career.save()

        if career is not None:

            messages.success(request, 'You Are Registered successfully!')

            return redirect('career')

        else:

            messages.success(request, 'You Are Not Registered !')

            return redirect('career')

    else:

            blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]

            mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

            articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

            vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

            headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

            trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]

            brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

            podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]

            Category=category.objects.filter(cat_status='active').order_by('order') [:12]

            # --------------ad-manage-meny--------------

            adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

            adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]



            adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

            adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]



            adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

            adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]



            adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

            adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]



            adrcol=ad_category.objects.get(ads_cat_slug='mrec')

            adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]



            # festivetop

            # festiveleft

            # festiveright

            # -------------end-ad-manage-meny--------------  

            # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

            

            slider=NewsPost.objects.filter().order_by('-id')[:5]

            latestnews=NewsPost.objects.all().order_by('-id')[:5]

            data={

                    'BlogData':blogdata,

                    'mainnews':mainnews,

                    'Slider':slider,

                    'Blogcat':Category,

                    'latnews':latestnews,

                    'adtop':adtop,

                    'adleft':adleft,

                    'adright':adright,

                    'adtl':adtopleft,

                    'adtr':adtopright,

                    'Articale':articales,

                    'vidart':vidarticales,

                    'headline':headline,

                    'trendpost':trending,

                    'bnews':brknews,

                    'vidnews':podcast,

                }

    return render(request,'inn/career.html',data)

# cat-career-page--end--------

   

# cat-Guestnewspost-page---------

@login_required(login_url="/login")

def Guestpost(request):

    if request.method == "POST":

        if 'upcoming_events' in request.POST:

            start_date = request.POST.get('start_date')

            end_date = request.POST.get('end_date')

        else:

            start_date = date.today()

            end_date = date.today()

            

        post_image = None

        if 'post_image' in request.FILES:

            post_image = request.FILES['post_image']

        

        postcat = request.POST.get('post_cat')

        post_title = request.POST.get('post_title')

        post_short_des = request.POST.get('post_short_des')

        post_des = request.POST.get('post_des')

        post_tag = request.POST.get('post_tag')

        is_active = request.POST.get('is_active')

        Head_Lines = request.POST.get('Head_Lines')

        articles = request.POST.get('articles')

        trending = request.POST.get('trending')

        brknews = request.POST.get('BreakingNews')

        newsch = request.POST.get('scheduled_datetime')

        order = request.POST.get('order')

        # counter = request.POST.get('counter')

        # status = request.POST.get('status')

        status = "inactive"

        upcoming_events=request.POST.get('upcoming_events')

        

        

        # Instantiate NewsPost with corrected fields

        newsdata = NewsPost(

            post_cat_id=postcat,

            post_title=post_title,

            post_short_des=post_short_des,

            post_des=post_des,

            post_image=post_image,

            post_tag=post_tag,

            is_active=is_active,

            Head_Lines=Head_Lines,

            articles=articles,

            trending=trending,

            BreakingNews=brknews,

            schedule_date=newsch,

            order=order,

            status=status,

            # post_status=counter,

            Event=upcoming_events,

            Event_date=start_date,

            Eventend_date=end_date,

            author_id = request.user.id

                )

        newsdata.save()

        if newsdata is not None:

            messages.success(request, 'Your news post successfully!')

            return redirect('guest-news-post')

        else:

            messages.success(request, 'You Are Not Registered !')

            return redirect('guest-news-post')

    else:

            blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]

            mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]

            articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

            vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

            headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]

            trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]

            brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

            podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]

            Category=category.objects.filter(cat_status='active').order_by('order') [:12]

            Categories=category.objects.filter(cat_status='active').order_by('order') [:11]

            # --------------ad-manage-meny--------------

            adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

            adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]



            adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

            adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]



            adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

            adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]



            adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

            adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]



            adrcol=ad_category.objects.get(ads_cat_slug='mrec')

            adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]



            slider=NewsPost.objects.filter().order_by('-id')[:5]

            latestnews=NewsPost.objects.all().order_by('-id')[:5]

            data={

                    'BlogData':blogdata,

                    'mainnews':mainnews,

                    'Slider':slider,

                    'Blogcat':Category,

                    'latnews':latestnews,

                    'adtop':adtop,

                    'adleft':adleft,

                    'adright':adright,

                    'adtl':adtopleft,

                    'adtr':adtopright,

                    'Articale':articales,

                    'vidart':vidarticales,

                    'headline':headline,

                    'trendpost':trending,

                    'bnews':brknews,

                    'vidnews':podcast,

                    'categories':Categories

                }

    return render(request,'inn/guestnewspost.html',data)

# cat-guestnewspost-page--end--------



# cat-EditNewsPost-page--start--------

@login_required(login_url="/login")

def EditNewsPost(request,post_id):

    blogdata=NewsPost.objects.get(id=post_id)

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    Categories=category.objects.filter(cat_status='active').order_by('order') [:11]

    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]

    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]

    data={

            'ed':blogdata,

            'categories':Categories,

            'Blogcat':Category,

            'trendpost':trending,

            'Articale':articales,

            }

    return render(request,'inn/edit-news-post.html',data)



# cat-updateNewsPost-page--start--------

@login_required(login_url="/login")

def UpdateNewsPost(request):

    if request.method == "POST":

        if 'upcoming_events' in request.POST:

            start_date = request.POST.get('start_date')

            end_date = request.POST.get('end_date')

        else:

            start_date = date.today()

            end_date = date.today()

            

        

        if 'post_image' in request.FILES:

            post_image = request.FILES['post_image']

        else:

            post_image =request.POST.get('post_image')

            

        post_id = request.POST.get('postId')

        postcat = request.POST.get('post_cat')

        post_title = request.POST.get('post_title')

        post_short_des = request.POST.get('post_short_des')

        post_des = request.POST.get('post_des')

        post_tag = request.POST.get('post_tag')

        is_active = request.POST.get('is_active')

        Head_Lines = request.POST.get('Head_Lines')

        articles = request.POST.get('articles')

        trending = request.POST.get('trending')

        brknews = request.POST.get('BreakingNews')

        newsch = request.POST.get('scheduled_datetime')

        order = request.POST.get('order')

        counter = request.POST.get('counter')

        status = "inactive"

        upcoming_events=request.POST.get('upcoming_events')

        

        # Instantiate NewsPost with corrected fields

        newsdata = NewsPost(

            id=post_id,

            post_cat_id=postcat,

            post_title=post_title,

            post_short_des=post_short_des,

            post_des=post_des,

            post_image=post_image,

            post_tag=post_tag,

            is_active=is_active,

            Head_Lines=Head_Lines,

            articles=articles,

            trending=trending,

            BreakingNews=brknews,

            schedule_date=newsch,

            order=order,

            status=status,

            post_status=counter,

            Event=upcoming_events,

            Event_date=start_date,

            Eventend_date=end_date,

            author_id = request.user.id,

            post_date=date.today()

                )

        newsdata.save()

        if newsdata is not None:

            messages.success(request, 'Your news post Update successfully!')

            return redirect('managepost')

        else:

            messages.success(request, 'Not Update Somthing Went Wrong !')

            return redirect('managepost')

    



# sitemap-us-page---------

# thanks-page---------

def thanks(request):

    blogdata=NewsPost.objects.all().order_by('-id') [:4]

    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    # festivetop

    # festiveleft

    # festiveright

# -------------end-ad-manage-meny--------------  

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

        }

   

    return render(request,'thanks.html',data)

# thanks-us-page---------







def SiteMap(request):

    blogdata=NewsPost.objects.all().order_by('-id') [:4]

    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    # festivetop

    # festiveleft

    # festiveright

# -------------end-ad-manage-meny--------------  

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'sitemapcat':Category,

        }

    return render(request,'sitemap.html',data)



# advertise-with-us-page---------

def advertise(request):

    blogdata=NewsPost.objects.all().order_by('-id') [:4]

    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:7]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    # festivetop

    # festiveleft

    # festiveright

# -------------end-ad-manage-meny--------------  

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

        }

   

    return render(request,'advertise-with-us.html',data)







def Adsinquiry(request):

    seo='voicesofuae'

    blogdata = NewsPost.objects.filter(

        is_active=1, status='active').order_by('-id')[:20]

    mainnews = NewsPost.objects.filter(status='active').order_by('order')[:4]

    articales = NewsPost.objects.filter(

        articles=1, status='active').order_by('-id')[:3]

    Category = category.objects.filter(

        cat_status='active').order_by('order')[:11]



    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value



    slider = NewsPost.objects.filter().order_by('-id')[:5]

    latestnews = NewsPost.objects.all().order_by('-id')[:5]

    data = {

            'indseo':seo,

            'BlogData': blogdata,

            'mainnews': mainnews,

            'Slider': slider,

            'Blogcat': Category,

            'latnews': latestnews,

            'Articale': articales,

        }



    if request.method == 'POST':

        name = request.POST.get('name')

        age = request.POST.get('age')

        Cross_Sector = request.POST.get('Cross_Sector')

        proof = request.FILES.get('proof')

        phone = request.POST.get('phone')

        email = request.POST.get('email')

        sent_date = request.POST.get('sent_date')

        country = request.POST.get('country')

        city = request.POST.get('city')

        description = request.POST.get('description')

        agree_terms = request.POST.get('agree_terms') == 'on' 

        agree_payment = request.POST.get('agree_payment') == 'on' 



        

        adsinquiry = AdsEnquiry(

            name=name,

            age=age,

            Cross_Sector = Cross_Sector,

            phone=phone,

            email=email,

            proof=proof,

            sent_date=sent_date,

            country=country,

            city=city,

            description=description,

            agree_terms=agree_terms,

            agree_payment=agree_payment,

            )

        adsinquiry.save()



        # Send email

        subject = "Inquiry Submitted Successfully"

        message = f"Dear {name},\n\nThank you for submitting your inquiry.\n\nBest regards,\nDXB news network"

        from_email = 'no-reply@newsibleasia.comm'

        recipient_list = [email]



        send_mail(subject, message, from_email, recipient_list)



        messages.success(request, 'Your request has been sent successfully.')

                                                                                 

    return render(request, 'adsinquiry.html', data)

    



def cms_detail(request, slug):

    page = get_object_or_404(CMS, slug=slug, status='active')

    

    page.viewcounter = (page.viewcounter or 0) + 1

    page.save(update_fields=['viewcounter'])



    blogdata=NewsPost.objects.all().order_by('-id') [:4]

    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]

    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]

    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]

    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]

    

    # --------------ad-manage-meny--------------

    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')

    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

    

    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')

    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

    

    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')

    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

    

    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')

    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

    

    adrcol=ad_category.objects.get(ads_cat_slug='mrec')

    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

    

    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

    Category=category.objects.filter(cat_status='active').order_by('order') [:12]

    slider=NewsPost.objects.filter().order_by('-id')[:5]

    latestnews=NewsPost.objects.all().order_by('-id')[:5]

    data={

            'BlogData':blogdata,

            'Slider':slider,

            'Blogcat':Category,

            'latnews':latestnews,

            'adtop':adtop,

            'adleft':adleft,

            'adright':adright,

            'adtl':adtopleft,

            'adtr':adtopright,

            'Articale':articales,

            'vidart':vidarticales,

            'headline':headline,

            'trendpost':trending,

            'bnews':brknews,

            'page': page,

        }



    return render(request, 'cms_page.html', data)



def robots_txt(request):

    content = """User-agent: *

Disallow: /admin/

Disallow: /accounts/

Disallow: /login/

Disallow: /logout/

Disallow: /register/

Disallow: /profile/

Disallow: /dashboard/

Disallow: /private/



Allow: /



Sitemap: https://www.newsibleasia.com/sitemap

"""

    return HttpResponse(content, content_type="text/plain")

def posts_by_tag(request, slug):
    current_datetime = datetime.now()
    tag = get_object_or_404(Tag, slug=slug)
    tagurl = f"/topic/{slug}"
    seo = seo_optimization.objects.filter(pageslug__iexact=tagurl, status='active').first()
   
    all_posts = NewsPost.objects.filter(tags=tag, status='active', schedule_date__lte=current_datetime).order_by('-schedule_date')
    paginator = Paginator(all_posts, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    all_video = VideoNews.objects.filter(tags=tag, is_active='active', schedule_date__lte=current_datetime).order_by('-schedule_date')[:10]
    video_page = Paginator(all_video, 8).get_page(request.GET.get('vpage'))
    user_agent = get_user_agent(request)
    is_mobile = user_agent.is_mobile

    categories = category.objects.filter(cat_status='active').order_by('order')[:12]
    articles = NewsPost.objects.filter(schedule_date__lte=current_datetime, articles=True, status='active').order_by('-id')[:12]

    context = {
        'indseo': seo,
        'tag': tag,
        'slugurl': tag.get_absolute_url(),
        'posts': page_obj,
        'video': video_page,
        'Blogcat': categories,
        'Articale': articles,
        'is_mobile': is_mobile,
    }
    return render(request, 'posts_by_tag.html', context)




def profiledxb(request, username ):

    current_datetime = datetime.now()

    profile_journalist = get_object_or_404(Journalist, username=username)



    journalist_articles = NewsPost.objects.filter(journalist=profile_journalist, articles=1, status='active').order_by('-id')[:6]

    galleries = profile_journalist.galleries.filter(status='active').order_by('-post_at')[:8]

    category_list = category.objects.filter(cat_status='active').order_by('order')[:12]

    journalist_blogdata = NewsPost.objects.filter(journalist=profile_journalist, status='active').order_by('-id')[:6]

    journalist_podcast = VideoNews.objects.filter(journalist=profile_journalist, is_active='active').order_by('-id')[:6]



    child_profiles = None

    recommended_profiles = None

    if profile_journalist.registration_type == 'organisation':

        org_code = profile_journalist.username

        child_profiles = Journalist.objects.filter(status='active', parent_organisations=org_code).order_by('-id')[:10]

    else:

        recommended_profiles = Journalist.objects.filter(status='active').exclude(id=profile_journalist.id).order_by('-id')[:10]



    # General blog and media

    blogdata = NewsPost.objects.filter(schedule_date__lt=current_datetime, is_active=1, status='active').order_by('-id')[:10]

    mainnews = NewsPost.objects.filter(schedule_date__lt=current_datetime, is_active=1, status='active').order_by('-id')[:2]

    articles = NewsPost.objects.filter(schedule_date__lt=current_datetime, articles=1, status='active').order_by('-id')[:3]

    headlines = NewsPost.objects.filter(schedule_date__lt=current_datetime, Head_Lines=1, status='active').order_by('-id')[:4]

    trending = NewsPost.objects.filter(schedule_date__lt=current_datetime, trending=1, status='active').order_by('-id')[:7]

    breaking = NewsPost.objects.filter(schedule_date__lt=current_datetime, BreakingNews=1, status='active').order_by('-id')[:8]

    podcast = VideoNews.objects.filter(is_active='active').order_by('-id')[:1]

    video_articles = VideoNews.objects.filter(articles=1, is_active='active', video_type='video').order_by('order')[:2]



    context = {

        'journalist': profile_journalist,

        'journalist_blogdata': journalist_blogdata,

        'journalist_articales': journalist_articles,

        'galleries': galleries,

        'Blogcat': category_list,

        'BlogData': blogdata,

        'mainnews': mainnews,

        'Articale': articles,

        'headline': headlines,

        'trendpost': trending,

        'bnews': breaking,

        'vidnews': podcast,

        'vidart': video_articles,

        'child_profiles': child_profiles,

        'recommended_profiles': recommended_profiles,

        'journalist_podcast': journalist_podcast,

    }



    return render(request, "inn/profile.html", context)

