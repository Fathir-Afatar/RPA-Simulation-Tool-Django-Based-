# Standard Application
import time
import openpyxl
import requests
import os

# Third-party
from bs4 import BeautifulSoup

# Django
from django.core.management.base import BaseCommand

BASE_URL = "http://127.0.0.1:8000"
EXCEL_PATH = "/home/fathir/Documents/web-target/media/reports/users_passwords.xlsx"

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

# Definisi warna ANSI
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"

class Command(BaseCommand):
    """A Django management command that automates user login, session handling,

    and report downloads via CSRF-protected web requests.
    """
    help = "Robot CLI for login and download report with CSRF"

    def add_arguments(self, parser):
        """Adds custom command-line arguments to the management command parser.

        Args:
            parser (argparse.ArgumentParser): The argument parser instance used
                to add command-line options.
        """
        parser.add_argument("--mode", choices=["single_month", "full_year"], default="single_month")
        parser.add_argument("--year", type=int, default=2025)
        parser.add_argument("--month", type=int, default=1) # default Januari

    def handle(self, *args, **options):
        """Executes the core logic of the management command.

        Iterates through users loaded from an Excel spreadsheet, performs
        authenticated sessions with CSRF token handling, and triggers report
        downloads based on the specified mode (single month or full year).
        Measures and outputs the execution benchmark upon completion.

        Args:
            *args: Variable length argument list.
            **options (dict): Arbitrary keyword arguments containing parsed CLI options
                (--mode, --year, --month).

        Raises:
            FileNotFoundError: If the target Excel file path cannot be located.
            requests.RequestException: If network requests to the target base URL fail.
        """
        mode = options["mode"]
        year = options["year"]
        month = options["month"]

        self.stdout.write("[*] Robot start...")
        start_time = time.time()

        wb = openpyxl.load_workbook(EXCEL_PATH)
        ws = wb.active

        total_users = 0
        total_files = 0

        for row in ws.iter_rows(min_row=2, values_only=True):
            username, password, pdf_password = row
            total_users += 1

            session = requests.Session()

            # Use login page to get CSRF
            login_page = session.get(f"{BASE_URL}/accounts/login/")
            soup = BeautifulSoup(login_page.text, "html.parser")
            csrf = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")

            # Send POST login with CSRF
            resp = session.post(f"{BASE_URL}/accounts/login/", data={
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrf,
            })
            self.stdout.write(f"{BLUE}[*] Login {username}... {RESET}")

            if "dashboard" in resp.url or resp.status_code == 200:
                self.stdout.write(f"{GREEN}     OK{RESET}")
                time.sleep(0.5)  # pause 0.5 seconds

                self.stdout.write(f"{YELLOW}     Open the Reports menu... OK{RESET}")
                time.sleep(0.5)  # pause 0.5 seconds

                self.stdout.write(f"{BLUE}    Select year {year}... OK{RESET}")
                time.sleep(0.5)  # pause 0.5 seconds

                self.stdout.write(f"{GREEN}     Click Filter... OK{RESET}")
                time.sleep(0.5)  # pause 0.5 seconds

                if mode == "single_month":
                    self.download_report(session, username, year, month, pdf_password, mode)
                    total_files += 1
                elif mode == "full_year":
                    for m in range(1, 13):
                        self.download_report(session, username, year, m, pdf_password, mode)
                        total_files += 1
                
                self.stdout.write(f"{GREEN}     back -> Dashboard -> Logout{RESET}")
                time.sleep(0.5)  # pause 0.5 seconds
            else:
                self.stdout.write(f"{YELLOW}        Login failed for {username}{RESET}")
                time.sleep(0.5)  # pause 0.5 seconds
        
        end_time = time.time()
        elapsed = end_time - start_time

        self.stdout.write("\n=== Bechmark ===")
        self.stdout.write(f"Mode: {mode}")
        self.stdout.write(f"Total users: {total_users}")
        self.stdout.write(f"Total files: {total_files}")
        self.stdout.write(f"Execution time: {elapsed:.2f} second")
    
    def download_report(self, session, username, year, month, pdf_password, mode):
        """Scrapes the reports page for a target user, locates the specified PDF link,

        downloads the file, and saves it to a structured local directory based on the execution mode.

        Args:
            session (requests.Session): The active HTTP session containing authentication cookies.
            username (str): The unique username of the target account being processed.
            year (int): The target report year.
            month (int): The target report month (1-12).
            pdf_password (str): The password required to decrypt or unlock the PDF file.
            mode (str): The execution mode determining the output folder structure
                ("single_month" or "full_year").

        Returns:
            None
        """
        # Take report page for specific year
        page = session.get(f"{BASE_URL}/reports/?year={year}")
        soup = BeautifulSoup(page.text, "html.parser")

        # Pattern file name: 1_protected.pdf, 2_protected.pdf, etc
        # Find link <a> that contains month name
        # Example, patter link : /media/reports/user1/2025/1_protected.pdf
        target_pattern = f"/media/reports/{username}/{year}/{month}_protected.pdf"
        link = soup.find("a", href=lambda h: h and target_pattern in h)
        if not link:
            self.stdout.write(f"{RED}    Failed to find a link for the month {month:02d}/{year} on {username}{RESET}")
            return

        pdf_url = BASE_URL + link["href"]

        # Make download folder accordingly to mode
        if mode == "single_month": # for 1 month
            folder = f"downloads/{MONTH_NAMES[month]} {year}"
        else: # full year (1 year)
            folder = f"downloads/{username}_{year}"
        
        os.makedirs(folder, exist_ok=True)
        file_path = f"{folder}/{username}_{MONTH_NAMES[month]}_{year}.pdf"

        # Simulation choosing month
        self.stdout.write(f"{GREEN}    Choose Month {month:02d}... OK{RESET}")
        time.sleep(0.5)  # pause 0.5 seconds

        self.stdout.write(f"{RED}    Click Download PDF... OK{RESET}")
        time.sleep(0.5)  # pause 0.5 seconds

        self.stdout.write(f"{YELLOW}    Input password PDF ({pdf_password})... OK{YELLOW}")
        time.sleep(0.5)  # pause 0.5 seconds

        self.stdout.write(f"{BLUE}    Click Submit... OK{RESET}")
        time.sleep(0.5)  # pause 0.5 seconds

        # Download file PDF
        r = session.get(pdf_url)
        if r.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(r.content)
            self.stdout.write(f"{BLUE}    File saved at {file_path}{RESET}")
            time.sleep(0.5)  # pause 0.5 seconds

            self.stdout.write(f"{YELLOW}    Return to Report Menu... OK{RESET}")
            time.sleep(0.5)  # pause 0.5 seconds
        else:
            self.stdout.write(f"{RED}    Failed to download PDF {MONTH_NAMES[month]} {year} for {username}{RESET}")
            time.sleep(0.5)  # pause 0.5 seconds

