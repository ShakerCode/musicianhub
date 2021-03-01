"""musicianhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from . import views
from .views import CreateBandView
# from .views import SearchView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='/'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('bands', views.bands, name='bands'),
    path('search_user', views.search_user, name='search_user'),
    path('search_band', views.search_band, name='search_band'),
    path('join_band', views.join_band, name='join_band'),
    path('leave_band', views.leave_band, name='leave_band'),
    # path('create_band', views.create_band, name='create_band'),
    path('create_band', CreateBandView.as_view(), name='create_band'),
    path('band/<int:pk>', views.band_profile, name='band_profile'),
    path('user/<int:pk>', views.user_profile, name='user_profile'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('messages/', include('django_messages.urls'))
    # django.contrib.auth.urls has built-in /login and /logout
]
