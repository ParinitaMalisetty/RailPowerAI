from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classify/basic/', views.classify_basic, name='classify_basic'),
    path('classify/scaled/', views.classify_scaled, name='classify_scaled'),
    path('forecast/basic/', views.forecast_basic, name='forecast_basic'),
    path('forecast/scaled/', views.forecast_scaled, name='forecast_scaled'),
]
