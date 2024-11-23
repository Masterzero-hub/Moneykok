from django.urls import path, include
from . import views

app_name = 'deposits'

urlpatterns = [
    path('', views.save_products, name="save_products"),
    path('classify/', views.classify, name='classify'),
    path('deposits-list/', views.deposits_list, name='deposits_list'),
    path('deposit-detail/<str:fin_prdt_cd>/', views.deposit_detail, name='deposit_detail'),
    path('deposit-detail/<str:fin_prdt_cd>/join/', views.deposit_join, name='deposit_join'),
]
