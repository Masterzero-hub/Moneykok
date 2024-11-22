from django.urls import path, include
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.communities, name='communities'),
    path('<int:article_pk>/', views.detail_update_delete, name='detail_update_delete'),
    path('<int:article_pk>/like/', views.like_article, name='like_article'),
    path('<int:article_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_update_delete, name='comment_update_delete'),
    path('profile/<str:user_id>/', views.profile, name='profile'),
]