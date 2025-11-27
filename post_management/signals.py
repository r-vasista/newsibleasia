# portals/signals.py
import requests
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import category, sub_category
from django.conf import settings

RECON_BASE_URL = settings.RECON_BASE_URL
PORTAL_NAME = settings.PORTAL_NAME

def sync_with_recon(endpoint, method="post", data=None):
    try:
        if method == "post":
            res = requests.post(RECON_BASE_URL + endpoint, json=data, timeout=5)
            print('request response is: ', res.json())
        elif method == "put":
            requests.put(RECON_BASE_URL + endpoint, json=data, timeout=5)
        elif method == "delete":
            requests.delete(RECON_BASE_URL + endpoint, timeout=5)
    except requests.RequestException as e:
        print(f"❌ Failed to sync with Recon: {e}")


@receiver(post_save, sender=sub_category)
def sync_sub_category(sender, instance, created, **kwargs):
    payload = {
        "portal_name": PORTAL_NAME,
        "external_id": str(instance.id),
        "name": instance.subcat_name,
        "parent_name": instance.sub_cat.cat_name if instance.sub_cat else None,   # 🔹 send parent
        "parent_external_id": str(instance.sub_cat.id) if instance.sub_cat else None,
    }
    print(payload, 'payload')
    if created:
        sync_with_recon("", "post", payload)
    else:
        sync_with_recon(f"{PORTAL_NAME}/{instance.id}/", "put", payload)


@receiver(post_delete, sender=sub_category)
def delete_sub_category(sender, instance, **kwargs):
    sync_with_recon(f"{PORTAL_NAME}/{instance.id}/", "delete")
