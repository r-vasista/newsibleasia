from django.db import models
import random
import string
import pycountry
from django_countries.fields import CountryField
from cities_light.models import Country, Region, City 
import phonenumbers
from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE


from django.core.mail import send_mail
from django.conf import settings


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Qualification(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CountryCode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dial_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.dial_code})"
    
    @classmethod
    def populate_country_codes(cls):
        """Fetch and store all country codes in the database with correct names."""
        existing_codes = set(cls.objects.values_list("dial_code", flat=True))  # Fetch existing dial codes

        for code, regions in _COUNTRY_CODE_TO_REGION_CODE.items():
            dial_code = f"+{code}"

            if dial_code in existing_codes:
                continue  # Skip duplicate country codes
            
            for region in regions:
                country = pycountry.countries.get(alpha_2=region)  # Get country by ISO code
                if country:
                    cls.objects.create(name=country.name, dial_code=dial_code)  # Direct insert
                    existing_codes.add(dial_code)  # Mark as inserted
                    break  # Only insert one country per dial code

    
class Journalist(models.Model):
    username = models.CharField(max_length=50, unique=True, blank=True)
    parent_organisations = models.CharField(max_length=155, null=True, blank=True)
    STATUS_CHOICES = (
        ('artist', 'Artist'),
        ('journalist', 'Journalist'),
        ('organisation', 'Organisation'),
    )
    registration_type = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    alternative_phone_number = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    state = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    languages = models.ManyToManyField(Language, blank=True)
    higher_education = models.ForeignKey(Qualification, on_delete=models.SET_NULL, blank=True, null=True)
    social_media_links = models.JSONField(default=dict, blank=True, null=True)
    selected_equipment = models.ManyToManyField(Equipment, blank=True)   
    passport_document = models.FileField(upload_to='documents/passport', blank=True, null=True)
    government_document = models.FileField(upload_to='documents/government/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    banner = models.ImageField(upload_to='banner/', blank=True, null=True)
    biography = models.TextField(blank=True, null=True, verbose_name="biography (max 120 characters)")
    terms_accepted = models.BooleanField(default=False)
    gallery_post_limit = models.PositiveIntegerField(default=8, verbose_name="Gallery Post Limit")
    password = models.CharField(max_length=128, default="defaultpassword")
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('approved', 'Approved'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):

        is_new = self._state.adding
        try:
            old_status = Journalist.objects.get(pk=self.pk).status
        except Journalist.DoesNotExist:
            old_status = None

        """Generate username automatically before saving."""
        if not self.username:
            self.username = self.generate_unique_username().upper() 
        super().save(*args, **kwargs)

        if old_status != self.status and not is_new:
            self.send_status_change_email()

    def send_status_change_email(self):
        if not self.email:
            return

        subject = ''
        message = ''

        if self.status == 'active':
            if self.registration_type == 'organisation':
                subject = 'Your ArtDomain Account is Now Active'
                message = (
                    f"Dear {self.organisation_name},\n\n"
                    f"Congratulations!\n\n"
                    f"Your institution has been officially approved under The Art Guild by ArtDomain, a project by DXB News Network. "
                    f"Account Summary:\n"
                    f"• Email: {self.email}\n"
                    f"• Username: {self.username}\n\n"
                    f"You are now ready to start onboarding your artists.\n\n"
                    f"This is not just a formality — it's a major opportunity to grow your presence and empower your creative community.\n\n"
                    f"What Your Artists Will Get:\n"
                    f"• Invite your artists to register through your institution.\n"
                    f"• Build your institution's unique identity — stand out from the crowd.\n"
                    f"• Give your artists a platform where they can gain real visibility and recognition.\n"
                    f"• Their own personal artist portal to upload exhibitions, awards, and updates.\n"
                    f"• A live, public profile available 24/7 for curators, collectors, and buyers worldwide.\n"
                    f"• Every approved update will be published as official news on DXB News Network.\n"
                    f"• Full support and visibility from your institution and ArtDomain when participating in exhibitions.\n\n"
                    f"Start onboarding your artists today and position your Art Guild as a leading voice in the world of contemporary art.\n\n"
                    f"If you need any assistance, our team is here to support you every step of the way.\n\n"
                    f"Warm regards,\n"
                    f"The ArtDomain Team\n"
                    f"DXB News Network"
                )
            else :
                subject = 'Your ArtDomain Account is Now Active'
                message = (
                    f"Hello {self.first_name} {self.last_name},\n\n"
                    f"Congratulations!\n\n"
                    f"Your {self.registration_type} account has been officially approved under The A-50 by ArtDomain, a project by DXB News Network.\n\n"
                    f"Account Summary:\n"
                    f"• Email: {self.email}\n"
                    f"• Username: {self.username}\n\n"
                    f"This approval marks an exciting opportunity to grow your artistic presence and connect with a wider creative community.\n\n"
                    f"Next Steps:\n"
                    f"• Sign in to your account using the link below:\n"
                    f"  🌐 https://www.newsibleasia.com/auth/sign-in\n"
                    f"• Update your profile\n\n"
                    f"If you need any assistance, our team is here to support you every step of the way.\n\n"
                    f"Warm regards,\n"
                    f"The ArtDomain Team\n"
                    f"📧 Contact Us: info@newsibleasia.com\n"
                    f"🌐 Website: www.newsibleasia.com"
                )

        elif self.status == 'inactive':
            subject = 'Your ArtDomain Account Has Been Deactivated'
            message = (
                f"Hello {self.first_name} {self.last_name},\n\n"
                f"We would like to inform you that your {self.registration_type} account has been temporarily deactivated as part of a routine review in line with our policies and procedures. "
                f"Our team is currently reviewing your account to ensure everything is in order.\n\n"
                f"If you have any questions or need further clarification, please feel free to reach out to us.\n\n"
                f"Account Summary:\n"
                f"• Email: {self.email}\n"
                f"• Username: {self.username}\n\n"
                f"Thank you for your patience and understanding. We will get back to you shortly with an update.\n\n"
                f"Warm regards,\n"
                f"The ArtDomain Team\n"
                f"📧 Contact Us: info@newsibleasia.com\n"
                f"🌐 Website: www.newsibleasia.com"
            )
        elif self.status == 'approved':
            subject = 'Your Journalist Account Has Been Approved'
            message = (
                f"Hello {self.first_name or self.username},\n\n"
                f"Congratulations!\n\n"
                f"Your {self.registration_type} account has been selected for ArtDomain by DXB News Network.\n"
                f"Our team will be reaching out to you shortly with further information and to guide you through the next steps for activating your account.\n\n"
                f"Account Summary:\n"
                f"• Email: {self.email}\n"
                f"• Username: {self.username}\n\n"
                f"If you have any questions in the meantime, feel free to contact us.\n\n"
                f"Warm regards,\n"
                f"The ArtDomain Team\n"
                f"📧 Contact Us: info@newsibleasia.com\n"
                f"🌐 Website: www.newsibleasia.com"
            )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=True,
        )

    def generate_unique_username(self):
        """Generate a username using the first 4 characters of first_name + 4 random digits."""
        first_part = (self.first_name[:4].lower() if self.first_name else "user")
        random_part = "".join(random.choices(string.digits, k=4))
        username = first_part + random_part

        while Journalist.objects.filter(username=username).exists():
            random_part = "".join(random.choices(string.digits, k=4))
            username = first_part + random_part

        return username

    def __str__(self):
        return self.username
#order




    

class Gallery(models.Model):
    journalist = models.ForeignKey('Journalist', on_delete=models.CASCADE, related_name="galleries")
    image = models.ImageField(upload_to="journalist", null=True, blank=True)
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')
    post_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gallery {self.id}"