from django.urls import path, include
from . import views

app_name = 'deposits'

urlpatterns = [
    path('save_products/', views.save_products, name="save_products"),

]
