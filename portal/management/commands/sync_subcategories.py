from django.core.management.base import BaseCommand
import requests

# Import your model
from post_management.models import sub_category  # adjust app/model name
from post_management.signals import PORTAL_NAME, RECON_BASE_URL  # reuse your constants


class Command(BaseCommand):
    help = "Sync all existing sub_category objects with Recon service"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🚀 Starting sub_category sync..."))

        total = sub_category.objects.count()
        success = 0
        failed = 0

        for sc in sub_category.objects.all():
            payload = {
                "portal_name": PORTAL_NAME,
                "external_id": str(sc.id),
                "name": sc.subcat_name,
                "parent_name": sc.sub_cat.cat_name if sc.sub_cat else None,   # 🔹 include parent name
                "parent_external_id": str(sc.sub_cat.id) if sc.sub_cat else None,  # 🔹 include parent id
            }

            try:
                res = requests.post(RECON_BASE_URL, json=payload, timeout=5)
                if res.status_code in [200, 201]:
                    success += 1
                else:
                    failed += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠️ Failed for {sc.id}: {res.status_code} - {res.text}"
                        )
                    )
            except requests.RequestException as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(f"❌ Request failed for {sc.id}: {e}")
                )

        self.stdout.write(self.style.SUCCESS("✅ Sync complete!"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Processed: {total}, Success: {success}, Failed: {failed}"
            )
        )
