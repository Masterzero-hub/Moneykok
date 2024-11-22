from django.urls import path, include
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.communities, name='communities'),
    path('<int:pk>/', views.detail, name='detail'),

]