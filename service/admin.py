from django.contrib import admin
from service.models import jobApplication, CareerApplication, SubscribeUser,BrandPartner,RegForm, AdsEnquiry, Contact
from django.contrib.auth.models import User
# Register your models here.

class jobApply(admin.ModelAdmin):
    list_display=(
        'category',
        'FullName',
        'education',
        'experience',
        'expsalary',
        'covernote',
        'status',
        'remark',
        'post_date',
        )
admin.site.register(jobApplication,jobApply)

class CareerApply(admin.ModelAdmin):
    list_display=(
            'name',
            'mobnumber',
            'email',
            'location',
            'nationality',
            'language',
            'address',
            'highestedu',
            'fos',
            'occupation',
            'journalexp',
            'lastwork',
            'portfolio',
            'category',
            'equipment',
            'softwareskill',
            'availability',
            'resume',
            'whyjoin',
            'anysegment',
            'status',
            'remark',
            'post_date',
            'is_active',
            )
admin.site.register(CareerApplication,CareerApply)

class subscriberAdmin(admin.ModelAdmin):
    list_display=(
            'name',
            'email',
            'ip',
            'country',
            'city',
            'subscribe_date',
            'is_active',
            )
admin.site.register(SubscribeUser,subscriberAdmin)

class bpAdmin(admin.ModelAdmin):
    list_display=(
            'name', 
            'email',
            'Logo',
            'url',
            'post_date',
            'is_active',
            )
admin.site.register(BrandPartner,bpAdmin)

class RegFormAdmin(admin.ModelAdmin):
    list_display=(
            'person_name',
            'company_name',
            'company_address',
            'phone',
            'email',
            'city',
            'country',
            'diesgantion',
            'enquiry_type',
            'executive_names',
            'source_from',
            'walk_in',
             'ip',
            'reg_date',
            'is_active',
            )
admin.site.register(RegForm,RegFormAdmin)



class AdsEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'Cross_Sector', 'phone', 'email', 'proof', 'sent_date', 'country', 'city', 'description', 'agree_terms', 'agree_payment' )
    list_filter = ('country', 'city')
    search_fields = ('name', 'age', 'phone', 'email', 'sent_date', 'country', 'city', 'description')

admin.site.register(AdsEnquiry, AdsEnquiryAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',  'email', 'subject', 'contact_date',)
    list_filter = ('contact_date', 'email',)
    search_fields = ('name', 'email', 'subject', 'contact_date')
admin.site.register(Contact, ContactAdmin)