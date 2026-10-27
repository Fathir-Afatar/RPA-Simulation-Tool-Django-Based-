from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('<int:year>/<int:month>', views.report_detail, name='report_detail'),
]