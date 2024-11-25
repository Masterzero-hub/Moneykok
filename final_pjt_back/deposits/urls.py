from django.urls import path, include
from . import views

app_name = 'deposits'

urlpatterns = [
    path('deposits-list/', views.deposits_list, name='deposits_list'),
    path('deposit-detail/<str:fin_prdt_cd>/', views.deposit_detail, name='deposit_detail'),
    path('deposit-detail/<str:fin_prdt_cd>/join/', views.deposit_join, name='deposit_join'),
    path('<int:joined_deposits_id>/delete/', views.joined_deposists_delete, name='joined_deposists_delete'),
    path('recommend-products/', views.recommend_products, name='recommend_products'),
]