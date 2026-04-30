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
    redeem_list,
    buy_package,
    tier_info,
    transaction_report,
    transactions_redeem,
    transactions_buy_package,
    transactions_tier_info,
    transactions_report,
    ajukan_klaim,
    riwayat_klaim,
    edit_klaim,
    batalkan_klaim,
    kelola_klaim,
    approve_klaim,
    reject_klaim,
    login_register,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_register, name='login_register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('members/list/', list_member, name='list_member'),
    path('members/add/', form_member, name='form_member'),
    path('members/redeem/', redeem_list, name='redeem_list'),
    path('members/buy-package/', buy_package, name='buy_package'),
    path('members/tier/', tier_info, name='tier_info'),
    path('members/transactions/', transaction_report, name='transaction_report'),
    # Transactions namespace (new)
    path('transactions/redeem/', transactions_redeem, name='transactions_redeem'),
    path('transactions/buy-package/', transactions_buy_package, name='transactions_buy_package'),
    path('transactions/tier/', transactions_tier_info, name='transactions_tier_info'),
    path('transactions/report/', transactions_report, name='transactions_report'),
    path('members/identitas/', list_identitas, name='list_identitas'),
    # Klaim URLs
    path('klaim/ajukan/', ajukan_klaim, name='ajukan_klaim'),
    path('klaim/riwayat/', riwayat_klaim, name='riwayat_klaim'),
    path('klaim/edit/<int:klaim_id>/', edit_klaim, name='edit_klaim'),
    path('klaim/batalkan/<int:klaim_id>/', batalkan_klaim, name='batalkan_klaim'),
    path('klaim/kelola/', kelola_klaim, name='kelola_klaim'),
    path('klaim/approve/<int:klaim_id>/', approve_klaim, name='approve_klaim'),
    path('klaim/reject/<int:klaim_id>/', reject_klaim, name='reject_klaim'),
]
