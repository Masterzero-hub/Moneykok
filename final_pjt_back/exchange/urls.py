from django.contrib import admin
from django.urls import path
from . import views

app_name="exchange"
urlpatterns = [
    path('', views.exchange, name='exchange')
]