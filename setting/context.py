from .models import profile_setting, CMS

def setting_context(request):
    return {
        'profile_setting': profile_setting.objects.first()
    }

def cms_context(request):
    return {
        'pages': CMS.objects.filter(status='active').order_by('order')
    }