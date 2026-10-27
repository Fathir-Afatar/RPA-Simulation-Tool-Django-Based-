from django.db import models
from django.contrib.auth.models import User

def user_report_path(instance, filename):
    """Generate a dynamic upload path for user-specific report files.

    This function structures the storage directory hierarchically based on the 
    associated user's username, report year, and month to keep files organized.

    Args:
        instance (Report): The model instance where the file is being attached.
            Must have a related `user` with a `username`, as well as `year` 
            and `month` attributes.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The structured file path string formatted as:
            `reports/{username}/{year}/{month}.pdf`
    """
    return f"reports/{instance.user.username}/{instance.year}/{instance.month}.pdf"

class Report(models.Model):
    """Represents an uploaded PDF report associated with a specific user.

    Attributes:
        user (ForeignKey): The user who owns the report. Cascades on deletion.
        year (IntegerField): The year corresponding to the report period.
        month (IntegerField): The month corresponding to the report period.
        file (FileField): The PDF file stored using the dynamic `user_report_path`.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    file = models.FileField(upload_to=user_report_path)

    def __str__(self):
        """Return a human-readable string representation of the report.

        Returns:
            str: Formatted string containing the username and month/year 
                (e.g., 'johndoe 10/2026').
        """
        return f"{self.user.username} - {self.month}/{self.year}"