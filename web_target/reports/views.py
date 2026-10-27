from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .models import Report
from datetime import datetime
import os

def report_list(request):
    user = request.user
    years = Report.objects.values_list('year', flat=True).distinct().order_by('-year')

    year = request.GET.get('year')
    months = []
    
    names = ['January', 'February', 'March', 'April', 'May', 'June',
                                    'July', 'August', 'September', 'October', 'November', 'December']
    
    current_month = datetime.now().month # ambil bulan sekarang
    
    for i, name in enumerate(names, start=1):
        report = None
        if year:
            report = Report.objects.filter(user=user, year=year, month=i).first()
        months.append({'value': i, 'name': name, 'report': report, 'is_current': (i == current_month)})

    return render(request, 'reports/report_list.html', {
        'years': years, # daftar untuk dropdown
        'year': year, # tahun yang dipilih
        'months': months,
        'report': report,
    })


def report_detail(request, year, month):
    report = Report.objects.filter(year=year, month=month).first()
    if report and report.file:
        # kirim file PDF sebagai response download
        return FileResponse(open(report.file.path, "rb"), content_type="application/pdf")
    return HttpResponse("Laporan tidak ditemukan.")
