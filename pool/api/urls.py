from django.urls import path, include
from rest_framework import routers

from pool.api import views

app_name = "pool_api"

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.VoucherAPIView.as_view()),
    path('verify/', views.VoucherValidationAPIView.as_view()),
    path('generate/', views.GenerateVoucherAPIView.as_view()),
]
