from django.urls import path, include
from . import views

app_name = 'deposits'

urlpatterns = [
    path('', views.save_products, name="save_products"),
    path('classify/', views.classify, name='classify'),
    path('deposits-list/', views.deposits_list, name='deposits_list'),
    path('deposit-detail/<str:fin_prdt_cd>/', views.deposit_detail, name='deposit_detail'),
    # path('products-all-list/', views.products_all_list, name="products_all_list"),
    # path('products-query-list/', views.products_query_list, name="products_query_list"),

]
