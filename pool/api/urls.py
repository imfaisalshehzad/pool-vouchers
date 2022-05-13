from django.urls import path, include
from rest_framework import routers

from pool.api import views

app_name = "pool_api"

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.VoucherAPIView.as_view(), name='email-return-voucher-codes'),
    path('verify/', views.VoucherValidationAPIView.as_view(), name='verify-voucher'),
    path('generate/', views.GenerateVoucherAPIView.as_view(), name='generate-voucher'),
    path('offers/', views.GenerateOffersAPIView.as_view(), name='generate-offers'),
]
