from django.urls import path, include
from . import views

app_name = 'deposits'

urlpatterns = [
    path('', views.save_products, name="save_products"),
    # path('products-all-list/', views.products_all_list, name="products_all_list"),
    # path('products-query-list/', views.products_query_list, name="products_query_list"),
    path('products-list/', views.products_list, name='products_list'),
    path('save-special-conditions/', views.save_special_conditions, name='save_special_conditions'),

]
