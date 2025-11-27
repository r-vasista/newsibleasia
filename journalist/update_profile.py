from .models import Journalist, Language, Equipment, CountryCode, Country, Region, City, Qualification
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
import random
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from post_management.models import category,sub_category,NewsPost,VideoNews
from cities_light.models import Country, Region, City
from phonenumbers import parse, is_valid_number, NumberParseException
from .models import CountryCode 
from django.db.models import Exists, OuterRef
from django.contrib import messages
from datetime import date, datetime
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password



def UpdateProfile(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', "").strip()
        last_name = request.POST.get('last_name', "").strip()
        country_code_id1 = request.POST.get("country_code")
        country_code_id2 = request.POST.get("alternative_country_code")
        phone_number = request.POST.get("phone_number", "").strip()
        alternative_phone_number = request.POST.get("alternative_phone_number", "").strip()

        country_code_obj1 = CountryCode.objects.filter(id=country_code_id1).first()
        full_phone_number = f"{country_code_obj1.dial_code}{phone_number}" if country_code_obj1 else phone_number

        country_code_obj2 = CountryCode.objects.filter(id=country_code_id2).first()
        full_alternative_phone_number = f"{country_code_obj2.dial_code}{alternative_phone_number}" if country_code_obj2 else alternative_phone_number

        journalist.first_name = first_name
        journalist.last_name = last_name
        journalist.phone_number = full_phone_number
        journalist.alternative_phone_number = full_alternative_phone_number
        journalist.save()

        return redirect('profile')

    country_codes = CountryCode.objects.all().order_by("name")

    return render(request, 'inn/Journalist_profile.html', {
        'journalist': journalist,
        'country_codes': country_codes,
    })



import base64
from django.core.files.base import ContentFile

def UpdateProfilePic(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        # Handle base64 cropped image
        cropped_image_data = request.POST.get('cropped_image')

        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,') 
            ext = format.split('/')[-1]  # "jpeg", "png", etc.
            data = ContentFile(base64.b64decode(imgstr), name=f"profile_{journalist_id}.{ext}")
            
            journalist.profile_picture = data
            journalist.save()
        
        return redirect('profile')

    return render(request, 'inn/Journalist_profile.html', {
        'journalist': journalist,
    })



import base64
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from .models import Journalist  # Adjust if your import differs

def UpdateBannerPic(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        image_data = request.POST.get("cropped_image")

        if image_data:
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f'banner_{journalist_id}.{ext}'
                banner_file = ContentFile(base64.b64decode(imgstr), name=file_name)
                journalist.banner = banner_file
                journalist.save()
            except Exception as e:
                print("Error saving banner:", e)

        return redirect('profile')

    return render(request, 'inn/Journalist_profile.html', {
        'journalist': journalist,
    })





def UpdateAddress(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        address_line1 = request.POST.get("address_line1")
        address_line2 = request.POST.get("address_line2")
        nationality = request.POST.get("nationality")
        state = request.POST.get("selected_state")
        city = request.POST.get("selected_city")
        zipcode = request.POST.get("zipcode")

        nationality_obj = Country.objects.filter(id=nationality).first() if nationality else None
        state_obj = Region.objects.filter(id=state).first() if state else None
        city_obj = City.objects.filter(id=city).first() if city else None

        journalist.address_line1 = address_line1
        journalist.address_line2 = address_line2
        journalist.nationality = nationality_obj
        journalist.state = state_obj
        journalist.city = city_obj
        journalist.zipcode = zipcode
        journalist.save()

        return redirect('profile')

    nationalities = Country.objects.only("id", "name").order_by("name")

    return render(request, 'inn/Journalist_profile.html', {
        "journalist": journalist,
        "nationalities": nationalities,
    })



def UpdateStrength(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        selected_language_ids = request.POST.getlist('selected_language[]')
        higher_education_name = request.POST.get("higher_education")
        biography = request.POST.get("biography")

        higher_education_obj = Qualification.objects.filter(name=higher_education_name).first()

        journalist.higher_education = higher_education_obj
        journalist.biography = biography
        journalist.save()

        journalist.languages.set(selected_language_ids)
        return redirect('profile')

    nationalities = Country.objects.only("id", "name").order_by("name")
    qualification = Qualification.objects.all()
    languages = Language.objects.all()

    return render(request, 'inn/Journalist_profile.html', {
        "journalist": journalist,
        "nationalities": nationalities,
        "qualification": qualification,
        "languages": languages,
    })



def UpdateEquipment(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        selected_equipment = request.POST.getlist("equipment[]")
        journalist.selected_equipment.set(selected_equipment)
        return redirect('profile')

    equipment = Equipment.objects.all()

    return render(request, 'inn/Journalist_profile.html', {
        "journalist": journalist,
        "equipments": equipment,
    })



def UpdateSocialMedia(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')

    if request.method == 'POST':
        social_media_links = {
            key.replace("social_media_links[", "").replace("]", ""): value.strip()
            for key, value in request.POST.items()
            if key.startswith("social_media_links[")
        }

        journalist.social_media_links = social_media_links
        journalist.save()

        return redirect('profile')

    return render(request, 'inn/Journalist_profile.html', {
        "journalist": journalist,
    })