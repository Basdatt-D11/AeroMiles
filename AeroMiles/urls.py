"""
URL configuration for AeroMiles project.

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
from django.urls import path
from members.views import (
    list_member,
    form_member,
    dashboard,
    list_identitas,
    login_page,
    logout_page,
    register_page,
    profile_settings,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/list/', list_member, name='list_member'),
    path('members/add/', form_member, name='form_member'),
    path('', dashboard, name='dashboard'),
    path('members/identitas/', list_identitas, name='list_identitas'),
    path('auth/login/', login_page, name='login_page'),
    path('auth/logout/', logout_page, name='logout_page'),
    path('auth/register/', register_page, name='register_page'),
    path('profile/settings/', profile_settings, name='profile_settings'),
]
