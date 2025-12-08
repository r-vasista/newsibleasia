from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import os

THUMBNAIL_SIZE = (400, 400)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


class Command(BaseCommand):
    help = "Automatically scan all image files inside MEDIA_ROOT and generate thumbnails"

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT

        if not os.path.isdir(media_root):
            self.stdout.write(self.style.ERROR(f"MEDIA_ROOT not found: {media_root}"))
            return

        created = 0
        skipped = 0
        failed = 0

        # Walk through all folders inside MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            # Make thumbnails folder inside each folder
            thumb_dir = os.path.join(root, "thumbnails")
            os.makedirs(thumb_dir, exist_ok=True)

            for filename in files:
                if not filename.lower().endswith(IMAGE_EXTENSIONS):
                    continue

                original_path = os.path.join(root, filename)
                thumb_path = os.path.join(thumb_dir, filename)

                # Skip if thumb exists
                if os.path.exists(thumb_path):
                    skipped += 1
                    continue

                try:
                    with Image.open(original_path) as img:
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")

                        img.thumbnail(THUMBNAIL_SIZE)
                        img.save(thumb_path, "JPEG", quality=85)

                        created += 1
                        self.stdout.write(self.style.SUCCESS(f"Thumbnail created: {thumb_path}"))

                except Exception as e:
                    failed += 1
                    self.stdout.write(
                        self.style.ERROR(f"Error generating thumbnail for {filename}: {e}")
                    )

        # Summary
        self.stdout.write(self.style.SUCCESS("----- SUMMARY -----"))
        self.stdout.write(self.style.SUCCESS(f"Created: {created}"))
        self.stdout.write(self.style.WARNING(f"Skipped: {skipped}"))
        self.stdout.write(self.style.ERROR(f"Failed: {failed}"))