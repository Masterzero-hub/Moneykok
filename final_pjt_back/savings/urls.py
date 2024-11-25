from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('savings-list/', views.savings_list, name='savings_list'),
    path('saving-detail/<str:fin_prdt_cd>/', views.savings_detail, name='saving_detail'),
    path('saving-detail/<str:fin_prdt_cd>/join/', views.savings_join, name='saving_join'),
    path('<int:joined_savings_id>/delete/', views.joined_savings_delete, name='joined_savings_delete'),
    path('recommend-products/', views.recommend_products, name='recommend_products'),
]
