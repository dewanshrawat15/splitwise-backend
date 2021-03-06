"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_auth import views as user_auth_views
from finance import views as finanace_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_auth_views.UserRegistration.as_view(), name='user_registration'),
    path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/token/', TokenObtainPairView.as_view(), name='token_access'),
    path('accounts/details/', finanace_views.FinanceAccount.as_view(), name='account_details'),
    path('transaction/', finanace_views.TransactionDetail.as_view(), name='transaction_view'),
    path('transaction/activity/', finanace_views.TransactionActivities.as_view(), name='transaction_view'),
]
