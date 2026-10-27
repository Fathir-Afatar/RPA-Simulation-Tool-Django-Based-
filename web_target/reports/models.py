from django.db import models
from django.contrib.auth.models import User

def user_report_path(instance, filename):
    # simpan file per user, per tahun, per bulan
    return f"reports/{instance.user.username}/{instance.year}/{instance.month}.pdf"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    file = models.FileField(upload_to=user_report_path)

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"