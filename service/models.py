from django.db import models
from post_management.models import category, sub_category
from django.contrib.auth.models import User
#from django import forms

# class YourModelAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.Model
#         fields = '__all__'
#         widgets = {
#             'post_title': forms.TextInput(attrs={'placeholder': 'Your Placeholder Text'}),
#             # Add other fields and their respective placeholder texts here if needed
#         }
  
# Create your models here.
class jobApplication(models.Model):
    category=models.ForeignKey(category, verbose_name="Select Category",null=True,default=None,on_delete=models.CASCADE)
    FullName=models.CharField(max_length=65, verbose_name="Name",null=True,default=None)
    education=models.CharField(max_length=100, verbose_name="Higher Education",null=True,default=None)
    
    experience=models.CharField(max_length=160, verbose_name="Work Experience",null=True,default=None)
    expsalary=models.CharField(max_length=160, verbose_name="Expected Salary",null=True,default=None)
    covernote=models.TextField(null=True,default='na',verbose_name="Cover Note")
    resume=models.FileField(upload_to="cv/", max_length=255,null=True,default=None)
    
    STATUS_CHOICES = (
        ('selected', 'Selected'),
        ('NotSelected', 'Not Selected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NotSelected')
    remark=models.TextField(null=True,default='na',verbose_name="Remark")
    post_date=models.DateTimeField(auto_now=True)
    
    
    
class CareerApplication(models.Model):
    name=models.CharField(max_length=100, verbose_name="Name",null=True,default=None)
    mobnumber=models.CharField(max_length=100, verbose_name="Contact Number",null=True,default=None)
    email=models.CharField(max_length=160, verbose_name="email",null=True,default=None)
    location=models.CharField(max_length=160, verbose_name="location",null=True,default=None)
    nationality=models.CharField(max_length=160, verbose_name="nationality",null=True,default=None)
    language=models.CharField(max_length=160, verbose_name="language",null=True,default=None)
    address=models.TextField(null=True,default='na',verbose_name="address")
    highestedu=models.CharField(max_length=100, verbose_name="Higher Education",null=True,default=None)
    fos=models.CharField(max_length=100, verbose_name="FieldOfStudy",null=True,default=None)
    occupation=models.CharField(max_length=160, verbose_name="occupation",null=True,default=None)
    journalexp=models.CharField(max_length=160, verbose_name="journalexp",null=True,default=None)
    lastwork=models.CharField(max_length=160, verbose_name="lastwork",null=True,default=None)
    portfolio=models.CharField(max_length=160, verbose_name="Portfolio",null=True,default=None)
    category=models.ForeignKey(sub_category, verbose_name="Select Category",null=True,default=None,on_delete=models.CASCADE)
    equipment=models.CharField(max_length=160, verbose_name="Equipment",null=True,default=None)
    softwareskill=models.CharField(max_length=160, verbose_name="Softwareskill",null=True,default=None)
    availability=models.CharField(max_length=160, verbose_name="Availability",null=True,default=None)
    resume=models.FileField(upload_to="cv/", max_length=255,null=True,default=None)
    whyjoin=models.TextField(null=True,default='na',verbose_name="Why Join")
    anysegment=models.TextField(null=True,default='na',verbose_name="Anysegment")
    STATUS_CHOICES = (
        ('selected', 'Selected'),
        ('NotSelected', 'Not Selected'),
    )
    status = models.CharField(max_length=20, null=True,choices=STATUS_CHOICES, default='NotSelected')
    remark=models.TextField(null=True,default='na',verbose_name="Remark")
    post_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name="Active", default=False)
    
class SubscribeUser(models.Model):
    name = models.CharField(max_length=255, null=True,verbose_name="Name")
    email = models.CharField(max_length=255, null=True,verbose_name="email")
    ip = models.CharField(max_length=255,null=False, verbose_name="User Ip")
    country = models.CharField(max_length=255,null=False, verbose_name="Country")
    city = models.CharField(max_length=255,null=False, verbose_name="City")
    subscribe_date = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name="Active", default=True)
    def __str__(self):
        return self.email
    
class BrandPartner(models.Model):
    name = models.CharField(max_length=255, null=True,verbose_name="Name")
    email = models.CharField(max_length=255, null=True,verbose_name="Email")
    Logo = models.FileField(upload_to="bplogo/", max_length=255,null=True,default=None)
    url = models.CharField(max_length=255,null=False, verbose_name="URL")
    post_date = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name="Active", default=True)
    def __str__(self):
        return self.name
    
class RegForm(models.Model):
        person_name= models.CharField(max_length=255, null=True,verbose_name="Person Name")
        company_name= models.CharField(max_length=255, null=True,verbose_name="Company Name")
        company_address= models.CharField(max_length=255, null=True,verbose_name="Company Address")
        phone= models.CharField(max_length=255, null=True,verbose_name="phone")
        email= models.CharField(max_length=255, null=True,verbose_name="email")
        city = models.CharField(max_length=255, null=True,verbose_name="city")
        country= models.CharField(max_length=255, null=True,verbose_name="country")
        diesgantion= models.CharField(max_length=255, null=True,verbose_name="Designation")
        enquiry_type= models.CharField(max_length=255, null=True,verbose_name="enquiry_type")
        executive_names= models.CharField(max_length=255, null=True,verbose_name="executive names")
        source_from=models.ForeignKey(sub_category, verbose_name="Select Category",null=True,default=None,on_delete=models.CASCADE)
        walk_in= models.CharField(max_length=255, null=True,verbose_name="walk_in")
        ip = models.CharField(max_length=255,null=False, verbose_name="User Ip")
        reg_date=models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        is_active=models.BooleanField(verbose_name="Active", default=True)
        def __str__(self):
            return self.email




class AdsEnquiry(models.Model):
        AGE_GROUPS = [
            ('young-children', 'Young Children (5–12y)'),
            ('teenagers', 'Teenagers (13–19y)'),
            ('young-adults', 'Young Adults (20–35y)'),
            ('adults', 'Adults (36–60y)'),
            ('senior-citizens', 'Senior Citizens (60+)'),
        ]

        SECTORS = [
            ('science-technology', 'Science and Technology'),
            ('entrepreneurship', 'Entrepreneurship'),
            ('environment', 'Environment and Sustainability'),
            ('social-media', 'Social Media and Content Creation'),
            ('health-wellness', 'Health and Wellness'),
            ('civic-engagement', 'Civic Engagement'),
            ('diversity-inclusion', 'Diversity and Inclusion'),
            ('spirituality', 'Spirituality and Philosophy'),
        ]

        name= models.CharField(max_length=255, null=True)
        age = models.CharField(max_length=20, null=True, blank=True, choices=AGE_GROUPS)
        Cross_Sector = models.CharField(max_length=20, null=True, blank=True, choices=SECTORS)
        phone= models.CharField(max_length=255, null=True,verbose_name="phone")
        email= models.CharField(max_length=255, null=True,verbose_name="email")
        country= models.CharField(max_length=255, null=True,verbose_name="country")
        city = models.CharField(max_length=255, null=True,verbose_name="city")
        description=models.TextField(null=True, blank=True)
        sent_date=models.DateTimeField(auto_now_add=True)
        proof = models.FileField(upload_to='proofs/')
        agree_terms = models.BooleanField(default=False)
        agree_payment = models.BooleanField(default=False)
        def _str_(self):
            return f'{self.name} - {self.email} - {self.phone}'
        

class Contact(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=155, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name
