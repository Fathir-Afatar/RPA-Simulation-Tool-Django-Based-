"""
URL configuration for web_target project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login),
    path('admin/', admin.site.urls),
    path('accounts/', include('web_target.accounts.urls')), # login, profil
    path('reports/', include('web_target.reports.urls')), # laporan PDF
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
