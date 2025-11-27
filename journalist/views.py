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

import logging
logger = logging.getLogger(__name__)
import re


@csrf_exempt
def check_email_exists(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            return JsonResponse({"exists": True, "message": "Invalid email format."}, status=400)

        email_exists = Journalist.objects.filter(email=email).exists()
        if email_exists:
            return JsonResponse({"exists": True, "message": "Email already exists! Use a different email."}, status=400)

        return JsonResponse({"exists": False, "message": "Email is available."})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def Send_OTP_Signup(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        session_key = f"otp_signup_{email}"
        stored_otp = request.session.get(session_key)

        if not stored_otp:
            stored_otp = str(random.randint(100000, 999999))
            request.session[session_key] = stored_otp
            request.session.set_expiry(600)

        # print(f"Generated OTP for {email}: {stored_otp}")

        send_mail(
            "Your Secure OTP for DXB News Network (Signup)",
            f"Hello,\n\nYour OTP for signup is: {stored_otp}.\n\nPlease use this code within 5 minutes. If you didn't request this, please ignore this email.\n\nThank you,\nDXB News Network Team",
            "no-reply@newsibleasia.com",
            [email],
            fail_silently=False,
        )
        return JsonResponse({"status": "success", "message": "OTP sent successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def Verify_OTP_Signup(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        entered_otp = request.POST.get("otp", "").strip()

        if not email or not entered_otp:
            return JsonResponse({"status": "error", "message": "Email and OTP are required"}, status=400)

        session_key = f"otp_signup_{email}"
        stored_otp = request.session.get(session_key)

        if stored_otp and stored_otp == entered_otp:
            try:
                del request.session[session_key]
            except KeyError:
                pass
            return JsonResponse({"status": "success", "message": "OTP verified successfully!"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid or expired OTP"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



def get_cities(request):
    """AJAX endpoint to get cities based on selected state"""
    state_id = request.GET.get("state_id")
    if not state_id:
        return JsonResponse({"cities": []}) 

    cities = City.objects.filter(region_id=state_id).only("id", "name").order_by("name")
    cities_list = [{"id": city.id, "name": city.name} for city in cities]
    return JsonResponse({"cities": cities_list})


def get_states(request):
    """AJAX endpoint to get states based on selected nationality (country)"""
    country_id = request.GET.get("country_id")
    states = Region.objects.filter(country_id=country_id).only("id", "name").order_by("name")
    states_list = [{"id": state.id, "name": state.name} for state in states]
    return JsonResponse({"states": states_list})


def Journalist_Sign_Up(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        parent_organisations = request.POST.get("parent_organisations")
        last_name = request.POST.get("last_name")
        registration_type = request.POST.get("registration_type")
        organisation_name = request.POST.get("organisation_name")
        email = request.POST.get("email", "").strip()
        country_code_id = request.POST.get("country_code") 
        country_code_id2 = request.POST.get("country_code") 
        phone_number = request.POST.get("phone_number", "").strip()
        alternative_phone_number = request.POST.get("alternative_phone_number")
        address_line1 = request.POST.get("address_line1")
        address_line2 = request.POST.get("address_line2")
        nationality = request.POST.get("nationality")
        state = request.POST.get("selected_state")
        city = request.POST.get("selected_city")
        zipcode = request.POST.get("selected_zipcode")
        language = request.POST.getlist("selected_language[]")
        higher_education = request.POST.get("higher_education")
        selected_equipment = request.POST.getlist("selected_equipment[]")
        profile_picture = request.FILES.get("profile_picture")
        passport_document = request.FILES.get("passport_document")
        government_document = request.FILES.get("government_document")
        biography = request.POST.get("message_type")
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        terms_accepted = "agree" in request.POST

        errors = {}

        social_media_links = {
            key.replace("social_media_links[", "").replace("]", ""): value.strip()
            for key, value in request.POST.items()
            if key.startswith("social_media_links[")
        }

        if len(password) < 6:
            errors["password"] = "Password must be at least 6 characters long."

        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if not terms_accepted:
            errors["agree"] = "Please accept the terms and conditions."

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)
        
        country_code_obj = CountryCode.objects.filter(id=country_code_id).first()
        country_code_obj2 = CountryCode.objects.filter(id=country_code_id2).first()
        full_phone_number = f"{country_code_obj.dial_code}{phone_number}" 
        full_alternative_phone_number = f"{country_code_obj2.dial_code}{alternative_phone_number}" 
        nationality_obj = Country.objects.filter(id=nationality).first() if nationality else None
        state_obj = Region.objects.filter(id=state).first() if state else None
        city_obj = City.objects.filter(id=city).first() if city else None
        higher_education_obj = Qualification.objects.filter(name=higher_education).first() if higher_education else None

        journalist = Journalist( 
            first_name=first_name,
            last_name=last_name,
            registration_type=registration_type,
            organisation_name=organisation_name,
            parent_organisations=parent_organisations,
            email=email,
            phone_number=full_phone_number,
            alternative_phone_number=full_alternative_phone_number,
            address_line1=address_line1,
            address_line2=address_line2,
            nationality=nationality_obj, 
            state=state_obj, 
            city=city_obj,
            zipcode=zipcode,
            higher_education=higher_education_obj,
            social_media_links=social_media_links,
            profile_picture=profile_picture,
            passport_document=passport_document,
            government_document=government_document,
            biography=biography,
            terms_accepted=terms_accepted,
            password=make_password(password), 
        )
        journalist.save()
        journalist.languages.set(language)
        journalist.selected_equipment.set(selected_equipment) 


        if registration_type == 'journalist':
            subject = 'DXB News Network/Artdomain – Your Application Has Been Successfully Received'
            message = (
                    f"Dear {journalist.first_name} {journalist.last_name},\n\n"
                    f"Thank you for submitting your application to ArtDomain, the world’s first editorial-powered art visibility ecosystem, proudly launched by DXB News Network.\n"
                    f"We have received your details and your application is currently under verification by our review team.\n\n"
                    f"Application Summary:\n"
                    f"• Email: {journalist.email}\n"
                    f"• Username: {journalist.username}\n\n"
                    f"Warm regards,\n"
                    f"DXB News Network Security Team\n"
                    f"📧 Contact Us: info@newsibleasia.com\n"
                    f"🌐 Website: www.newsibleasia.com"
                )

            from_email = 'no-reply@newsibleasia.com'
            recipient_list = [journalist.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        else:
            subject = 'DXB News Network/Artdomain – Your Application Has Been Successfully Received'
            message = (
                    f"Dear {journalist.first_name} {journalist.last_name},\n\n"
                    f"Thank you for submitting your application to ArtDomain, the world’s first editorial-powered art visibility ecosystem, proudly launched by DXB News Network.\n"
                    f"We have received your details and your application is currently under verification by our review team.\n\n"
                    f"Application Summary:\n"
                    f"• Email: {journalist.email}\n"
                    f"• Username: {journalist.username}\n\n"
                    f"Important (For A50 – The Art Order Applicants):\n"
                    f"If you have applied as an individual artist for A50, please note\n"
                    f"• Only 50 artists globally are selected each year\n"
                    f"• Selection is based on first-come-first-reviewed, but also includes evaluation of:\n"
                    f"     • Originality and uniqueness of your artwork\n"
                    f"     • Years of professional artistic activity\n"
                    f"     • Presentation and seriousness of your portfolio\n\n"
                    f"If your profile is shortlisted, you will receive:\n"
                    f"• A formal approval email\n"
                    f"• An official PDF with next steps\n"
                    f"• A membership fee payment link (AED 3,500 per year)\n"
                    f"• And final verification of submitted documents\n\n"
                    f"Note: Once approved, if you choose not to proceed, your profile will be permanently blacklisted from all future   art-related opportunities at DXB News Network, including exhibitions,\n\n"
                    f"campaigns, or media partnerships. This platform is for committed creators only. A50 registration opens only once a year,  and only for 50 deserving individuals. We urge you to carefully review the attached official PDF document before proceeding  further.\n\n"

                    f"(For Institutions – The Art Guild):\n"
                    f"If you are applying as an institution, gallery, curator, or agency, the above conditions regarding artist selection and   limits do not apply.\n\n"
                    f"You may proceed with institutional onboarding as guided in the official document.\n\n"
                    f"If you have any questions, feel free to reach out to our support team.\n\n"

                    f"Warm regards,\n"
                    f"DXB News Network Security Team\n"
                    f"📧 Contact Us: info@newsibleasia.com\n"
                    f"🌐 Website: www.newsibleasia.com"
                )
            from_email = 'no-reply@newsibleasia.com'
            recipient_list = [journalist.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return JsonResponse(
            {
                "status": "success",
                "message": "Registration successful! Redirecting...",
                "redirect_url": reverse("sign-in"),
            },
            status=200,
        )
    
    equipment = Equipment.objects.all()
    language = Language.objects.all()
    Qualifications = Qualification.objects.all()
    country_codes = CountryCode.objects.all().order_by("name")
    nationalities = Country.objects.only("id", "name").order_by("name")
    Category = category.objects.filter(cat_status="active").order_by("order")[:11]
    trending = NewsPost.objects.filter(trending=1, status="active").order_by("-id")[:3]
    articles = NewsPost.objects.filter(articles=1, status="active").order_by("-id")[:3]
    registered_organizations = Journalist.objects.filter(status='active', registration_type='organisation')

    data = {
        "languages": language,
        "equipments": equipment,
        "qualification": Qualifications,
        "categories": Category,
        "trendpost": trending,
        "articles": articles,
        "nationalities": nationalities,
        "country_codes": country_codes,
        "registered_organizations": registered_organizations,
    }
    return render(request, "inn/Journalist_sign_up.html", data)


def Journalist_SignIn(request):
    if request.method == "POST":
        login_input = request.POST.get('login_input', "").strip()
        password = request.POST.get('password', "").strip()

        errors = {}

        if not login_input:
            errors["email"] = "Please enter your username or email."

        if not password:
            errors["password"] = "Password is required."

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        try:
            if '@' in login_input:
                journalist = Journalist.objects.get(email=login_input)
            else:
                journalist = Journalist.objects.get(username=login_input)

            if not check_password(password, journalist.password):
                return JsonResponse({"status": "error", "message": "Invalid password"}, status=401)

            if journalist.status == "inactive":
                subject = 'Account Under Verification - DXB News Network'
                message = (
                    f"Dear {journalist.first_name} {journalist.last_name},\n\n"
                    f"We would like to inform you that your account is currently under verification. "
                    f"As a result, you are unable to access certain features of the platform until the verification process is complete.\n\n"
                    f"If you have any concerns or questions, please do not hesitate to reach out to us at info@newsibleasia.com.\n\n"
                    f"We appreciate your patience and understanding during this process.\n\n"
                    f"Best regards,\n"
                    f"DXB News Network Team\n"
                    f"Contact Us: info@newsibleasia.com\n"
                    f"Website: www.newsibleasia.com"
                )

                from_email = 'no-reply@newsibleasia.com'
                recipient_list = [journalist.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return JsonResponse({
                    "status": "error", 
                    "message": "Your account is under verification. Please check your email for more details."
                }, status=403)

            request.session['journalist_id'] = journalist.id
            request.session.set_expiry(86400) 

            ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')

            subject = 'Security Alert: Successful Journalist Login Notification'
            message = (
                f"Dear {journalist.first_name} {journalist.last_name},\n\n"
                f"We would like to inform you that a successful login to your account was made on {journalist.email}.\n\n"
                f"Details of the login attempt:\n"
                f"• Email: {journalist.email}\n"
                f"• Username: {journalist.username} | IP: {ip_address} | User Agent: {user_agent}\n\n"
                f"If you did not initiate this action, we strongly advise you to immediately change your password and secure your account.\n\n"
                f"Should you have any concerns or require assistance, please do not hesitate to contact us.\n\n"
                f"Best regards,\n"
                f"DXB News Network Security Team\n"
                f"Contact Us: info@newsibleasia.com\n"
                f"Website: www.newsibleasia.com"
            )

            from_email = 'no-reply@newsibleasia.com'
            recipient_list = [journalist.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return JsonResponse(
                {
                "status": "success",
                "message": "Login successful! Redirecting...",
                "redirect_url": reverse("dashboard"),
                },
                status=200,
            )

        except Journalist.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid login credentials"}, status=401)

    return render(request, 'inn/Journalist_sign_in.html')


from django.urls import reverse
signer = TimestampSigner()
def Journalist_Forgot_Password(request):
    if request.method == 'POST':
        email = request.POST.get('email', "").strip()
        # print(f"Email received: {email}")

        try:
            journalist = Journalist.objects.get(email__iexact=email)
            token = signer.sign(journalist.id)
            reset_url = request.build_absolute_uri(reverse('Journalist-reset-password', args=[token]))

            subject = 'DXB News Network: Password Reset Request'
            message = (
                f"Dear {journalist.first_name} {journalist.last_name},\n\n"
                f"We have received a request to reset your password for your account on DXB News Network.\n\n"
                f"To reset your password, please click on the following link:\n"
                f"{reset_url}\n\n"
                f"If you did not initiate this request, please disregard this email and your account remains secure.\n\n"
                f"Best regards,\n"
                f"DXB News Network Security Team"
                f"Contact Us: info@newsibleasia.com\n"
                f"Website: www.newsibleasia.com"
            )
            from_email = 'no-reply@newsibleasia.com'
            recipient_list = [journalist.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return JsonResponse({"status": "success", "message": "Reset link has been sent to your email."}, status=200)

        except Journalist.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid email address."}, status=400)

    return render(request, 'inn/Journalist_forgot_password.html')



signer = TimestampSigner()
def Journalist_Reset_Password(request, token):
    try:
        journalist_id = signer.unsign(token, max_age=300)
        journalist = get_object_or_404(Journalist, id=journalist_id)

        if request.method == 'POST':
            new_password = request.POST.get('password', "").strip()
            confirm_password = request.POST.get('confirm_password', "").strip()
            errors = {}

            # **VALIDATIONS**
            if not new_password or not confirm_password:
                errors["password"] = "Password fields cannot be empty."

            if len(new_password) < 6:
                errors["password_length"] = "Password must be at least 6 characters long."

            if new_password != confirm_password:
                errors["password_mismatch"] = "Passwords do not match."

            # If there are errors, return JSON response
            if errors:
                return JsonResponse({"status": "error", "errors": errors}, status=400)

            # If all validations pass, update the password
            journalist.password = make_password(new_password)
            journalist.save()

            # Send confirmation email
            subject = 'DXB News Network: Password Reset Successfully'
            message = (
                f"Dear {journalist.first_name} {journalist.last_name},\n\n"
                f"Your password has been successfully reset.\n\n"
                f"If you did not perform this action, please contact support immediately.\n\n"
                f"Best regards,\n"
                f"DXB News Network Security Team"
                f"Contact Us: info@newsibleasia.com\n"
                f"Website: www.newsibleasia.com"   
            )
            from_email = 'no-reply@newsibleasia.com'
            recipient_list = [journalist.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return JsonResponse({
                "status": "success",
                "message": "Your password has been reset successfully.",
                "redirect_url": reverse("sign-in"),
            }, status=200)

        return render(request, 'inn/Journalist_reset_password.html', {'token': token})

    except (BadSignature, SignatureExpired):
        messages.error(request, "The reset link is invalid or has expired.")
        return JsonResponse({
            "status": "error",
            "message": "The reset link is invalid or has expired.",
            "redirect_url": reverse("Journalist_Forgot_Password"),
        }, status=400)


def Journalist_Dashboard(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')
    
    profile_journalist = get_object_or_404(Journalist, id=journalist_id)
    
    current_datetime = datetime.now()
    events=NewsPost.objects.filter(schedule_date__lt=current_datetime,Event=1,status='active').order_by('-id')[:10]

    total_active_posts = NewsPost.objects.filter(journalist=journalist, status='active').order_by('-id')
    total_active_posts_count = total_active_posts.count()
    total_inactive_posts = NewsPost.objects.filter(journalist=journalist, status='inactive').count()
    total_rejected_posts = NewsPost.objects.filter(journalist=journalist, status='rejected').count()

    total_active_articles = NewsPost.objects.filter(journalist=journalist, status='active', articles=1).order_by('-id')
    total_active_articles_count = total_active_articles.count()

    all_videos_post = VideoNews.objects.filter(journalist=journalist,).order_by('-id')
    active_video_type = VideoNews.objects.filter(is_active='active', video_type='video', journalist=journalist,).order_by('-id')
    inactive_video_type = VideoNews.objects.filter(is_active='inactive', video_type='video', journalist=journalist,).order_by('-id')
    rejected_video_type = VideoNews.objects.filter(is_active='rejected', video_type='video', journalist=journalist,).order_by('-id')
    active_reels_type = VideoNews.objects.filter(is_active='active', video_type='reel', journalist=journalist,).order_by('-id')
    inactive_reels_type = VideoNews.objects.filter(is_active='inactive', video_type='reel', journalist=journalist,).order_by('-id')
    rejected_reels_type = VideoNews.objects.filter(is_active='rejected', video_type='reel', journalist=journalist,).order_by('-id')
    all_videos_post_count = all_videos_post.count()
    active_reels_count = active_reels_type.count()
    inactive_reels_count = inactive_reels_type.count()
    rejected_reels_count = rejected_reels_type.count()
    active_video_count = active_video_type.count()
    inactive_video_count = inactive_video_type.count()
    rejected_video_count = rejected_video_type.count()

    blogdata = NewsPost.objects.filter(journalist=journalist, is_active=1).order_by('-id')[:20]
    mainnews = NewsPost.objects.filter(journalist=journalist, status='active').order_by('order')[:4]
    articales = NewsPost.objects.filter(journalist=journalist, articles=1, status='active').order_by('-id')[:3]
    headline = NewsPost.objects.filter(journalist=journalist, Head_Lines=1, status='active').order_by('-id')[:14]
    trending = NewsPost.objects.filter(journalist=journalist, trending=1, status='active').order_by('-id')[:3]
    brknews = NewsPost.objects.filter(journalist=journalist, BreakingNews=1, status='active').order_by('-id')[:8]
    slider = NewsPost.objects.filter(journalist=journalist).order_by('-id')[:5]
    latestnews = NewsPost.objects.filter(journalist=journalist).order_by('-id')[:5]
    vidarticales = VideoNews.objects.filter(articles=1, is_active='active', video_type='video').order_by('order')[:2]
    podcast = VideoNews.objects.filter(is_active='active').order_by('-id')[:1]
    Category = category.objects.filter(cat_status='active').order_by('order')[:11]
    Categories = category.objects.filter(cat_status='active').order_by('order')[:11]

    child_profiles = None
    if profile_journalist.registration_type == 'organisation':
        org_code = profile_journalist.username
        child_profiles = Journalist.objects.filter(status='active', parent_organisations=org_code).order_by('-id')[:10]
    
    data = {
        'BlogData':blogdata,
        'events':events,
        'mainnews':mainnews,
        'Slider':slider,
        'Blogcat':Category,
        'latnews':latestnews,
        'Articale':articales,
        'vidart':vidarticales,
        'headline':headline,
        'trendpost':trending,
        'bnews':brknews,
        'vidnews':podcast,
        'categories':Categories,
        'journalist': journalist,

        'total_active_posts': total_active_posts,
        'total_active_posts_count': total_active_posts_count,
        'total_active_articles_count': total_active_articles_count,
        'total_active_articles': total_active_articles,

        'active_video_type': active_video_type,
        'active_reels_type': active_reels_type,
        'active_video_count': active_video_count,
        'active_reels_count': active_reels_count,
        
        'total_rejected_posts': total_rejected_posts,
        'total_inactive_posts': total_inactive_posts,
        'child_profiles': child_profiles,
    }
    return render(request, 'inn/Journalist_dashboard.html', data)


def Journalist_Profile(request):
    journalist_id = request.session.get('journalist_id')
    if not journalist_id:
        return redirect('sign-in')

    try:
        journalist = Journalist.objects.get(id=journalist_id)
    except Journalist.DoesNotExist:
        return redirect('sign-in')
    
    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    Categories=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    country_codes = CountryCode.objects.all().order_by("name")
    nationalities = Country.objects.only("id", "name").order_by("name")
    language = Language.objects.all()
    Qualifications = Qualification.objects.all()
    equipment = Equipment.objects.all()
    
    data = {
        'BlogData':blogdata,
        'mainnews':mainnews,
        'Slider':slider,
        'Blogcat':Category,
        'latnews':latestnews,
        'Articale':articales,
        'vidart':vidarticales,
        'headline':headline,
        'trendpost':trending,
        'bnews':brknews,
        'vidnews':podcast,
        'categories':Categories,
        'journalist': journalist,
        'country_codes': country_codes,
        "nationalities": nationalities,
        "languages": language,
        "qualification": Qualifications,
        "equipments": equipment,
    }
    return render(request, 'inn/Journalist_profile.html', data)


def logout_view(request):
    credentials = ['journalist_email', 'journalist_username', 'journalist_id']
    for shinu in credentials:
        if shinu in request.session:
            del request.session[shinu]

    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

