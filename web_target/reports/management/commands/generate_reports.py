from django.conf import settings
from pathlib import Path
from reportlab.pdfgen import canvas
import pikepdf
from django.contrib.auth.models import User
from web_target.reports.models import Report
from django.core.management.base import BaseCommand
from openpyxl import Workbook


class Command(BaseCommand):
    help = "Generate dummy users and PDF reports"

    def handle(self, *args, **options):
        total_users = 5
        years = [2025, 2026]

        user_data = []
        for i in range(1, total_users+1):
            username = f"user{i}"
            password = f"user{i}pass"
            pdf_password = password

            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()

            for year in years:
                for month in range(1, 13):
                    folder = settings.MEDIA_ROOT / "reports" / username / str(year)
                    folder.mkdir(parents=True, exist_ok=True)
                    file_path = folder / f"{month}.pdf"

                    # Generate PDF plain
                    c = canvas.Canvas(str(file_path))
                    c.drawString(100, 750, f"Monthly Report {month} Year {year} for {username}")
                    print(f"Writing file to: {file_path.resolve()}")
                    c.save()
                    print(f"Completed file: {file_path.resolve()}")

                    # Encrypt PDF
                    protected_path = folder / f"{month}_protected.pdf"
                    with pikepdf.open(file_path) as pdf:
                        pdf.save(
                            protected_path,
                            encryption=pikepdf.Encryption(owner="ownerpass", user=pdf_password)
                        )

                    # Simpan ke model
                    Report.objects.get_or_create(
                        user=user,
                        year=year,
                        month=month,
                        file=f"reports/{username}/{year}/{protected_path.name}"
                    )

                    self.stdout.write(self.style.SUCCESS(
                        f"Report {month}/{year} for {username} finished being made."
                    ))
                    user_data.append({"username": username, "password": password, "pdf_password": pdf_password})

        # setelah semua selesai -> export Excel
        excel_file = export_users_excel(user_data)
        self.stdout.write(self.style.SUCCESS(f"Excel file dibuat: {excel_file}"))

def export_users_excel(user_data):
    # user_data  list of dict {username, password, pdf_password}
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    # Header
    ws.append(["Username", "Password", "PDF Password"])

    # Isi data
    for row in user_data:
        ws.append([row["username"], row["password"], row["pdf_password"]])

    # Path file Excel
    excel_path = settings.MEDIA_ROOT / "reports" / "users_passwords.xlsx"
    wb.save(excel_path)
    return excel_path