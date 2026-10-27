from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from web_target.reports.models import Report
from django.conf import settings
import shutil

class Command(BaseCommand):
    help = "Reset dummy users, reports, and PDF files"

    def handle(self, *args, **options):
        # Hapus semua report
        Report.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All reports have been deleted."))

        # Hapus semua user dummy (user1..userN)
        User.objects.filter(username__startswith="user").delete()
        self.stdout.write(self.style.SUCCESS("All dummy users have been deleted."))

        # Hapus folder reports di media
        reports_dir = settings.MEDIA_ROOT / "reports"
        if reports_dir.exists():
            shutil.rmtree(reports_dir)
            self.stdout.write(self.style.SUCCESS("The 'reports' folder in the media directory has been deleted."))

        self.stdout.write(self.style.SUCCESS("The database and dummy folders have been cleared."))
