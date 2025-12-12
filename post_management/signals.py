# portals/signals.py
import requests
import os
from PIL import Image
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import category, sub_category, NewsPost
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

THUMBNAIL_SIZE = (400, 400)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


@receiver(post_save, sender=NewsPost)
def run_thumbnail_logic_on_new_post(sender, instance, created, **kwargs):
    """
    Generate a single WEBP thumbnail when a new NewsPost is created.
    """

    if not created:
        return   # Only for newly created posts

    if not instance.post_image:
        return

    original_path = instance.post_image.path
    root = os.path.dirname(original_path)
    filename = os.path.basename(original_path)

    thumb_dir = os.path.join(root, "thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)

    # Final thumbnail name: same base name, but .webp extension
    base_name, _ = os.path.splitext(filename)
    webp_thumb_path = os.path.join(thumb_dir, f"{base_name}.webp")

    # Skip if exists
    if os.path.exists(webp_thumb_path):
        return

    try:
        with Image.open(original_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail(THUMBNAIL_SIZE)

            # Save ONLY in WEBP format
            img.save(webp_thumb_path, "WEBP", quality=85, method=6)

            print("WEBP Thumbnail Created:", webp_thumb_path)

    except Exception as e:
        print("Thumbnail Error:", e)