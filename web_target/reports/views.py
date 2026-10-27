# Standard Library
from datetime import datetime
import os

# Django
from django.shortcuts import render
from django.http import HttpResponse, FileResponse

# Local Application
from .models import Report


def report_list(request):
    """Render the report list view with year filters and monthly report mapping.

        This view retrieves distinct available report years for dropdown selection,
        processes the currently selected year filter, and maps all 12 months with 
        their corresponding report objects and current-month status for the user.

        Args:
            request (HttpRequest): The HTTP request object containing user session 
                and GET query parameters (e.g., 'year').

        Returns:
            HttpResponse: The rendered HTML response containing the report list 
                template, context with available years, selected year, mapped months, 
                and the last processed report object.
    """
    user = request.user
    years = Report.objects.values_list('year', flat=True).distinct().order_by('-year')

    year = request.GET.get('year')
    months = []
    
    names = ['January', 'February', 'March', 'April', 'May', 'June',
                                    'July', 'August', 'September', 'October', 'November', 'December']
    
    current_month = datetime.now().month
    
    for i, name in enumerate(names, start=1):
        report = None
        if year:
            report = Report.objects.filter(user=user, year=year, month=i).first()
        months.append({'value': i, 'name': name, 'report': report, 'is_current': (i == current_month)})

    return render(request, 'reports/report_list.html', {
        'years': years, 
        'year': year,
        'months': months,
        'report': report,
    })


def report_detail(request, year, month):
    """Serve a specific PDF report file as an inline download response.

        Queries the database for a report matching the given year and month. If found 
        and the file exists on disk, it streams the PDF file back to the client 
        using a FileResponse. Otherwise, returns a 404-style text response.

        Args:
            request (HttpRequest): The HTTP request object.
            year (int): The target year of the report.
            month (int): The target month number (1-12) of the report.

        Returns:
            FileResponse: Streaming HTTP response with 'application/pdf' content type 
                if the report file exists.
            HttpResponse: Plain text error response ('Laporan tidak ditemukan.') if 
                the report or file is missing.
    """
    report = Report.objects.filter(year=year, month=month).first()
    if report and report.file:
        # kirim file PDF sebagai response download
        return FileResponse(open(report.file.path, "rb"), content_type="application/pdf")
    return HttpResponse("Laporan tidak ditemukan.")
