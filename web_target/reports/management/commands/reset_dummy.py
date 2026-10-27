# Standard Library
import shutil

# Django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

# Local Application
from web_target.reports.models import Report


class Command(BaseCommand):
    """A Django management command that resets the environment by clearing all dummy

    reports from the database, deleting dummy user accounts, and removing the
    generated reports directory from the media storage.
    """
    help = "Reset dummy users, reports, and PDF files"

    def handle(self, *args, **options):
        """Executes the reset logic to purge database records and media files.

        Deletes all `Report` instances, removes user accounts whose usernames
        start with the "user" prefix, and recursively deletes the 'reports'
        folder located within the Django MEDIA_ROOT directory.

        Args:
            *args: Variable length argument list.
            **options (dict): Arbitrary keyword arguments passed by the command-line parser.

        Returns:
            None
        """
        # Delete all report
        Report.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All reports have been deleted."))

        # Delete all dummy user
        User.objects.filter(username__startswith="user").delete()
        self.stdout.write(self.style.SUCCESS("All dummy users have been deleted."))

        # Delete reports folder in media
        reports_dir = settings.MEDIA_ROOT / "reports"
        if reports_dir.exists():
            shutil.rmtree(reports_dir)
            self.stdout.write(self.style.SUCCESS("The 'reports' folder in the media directory has been deleted."))

        self.stdout.write(self.style.SUCCESS("The database and dummy folders have been cleared."))
