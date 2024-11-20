from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/send-code-email/', views.send_code_email, name='send_code_email'),
    path('signup/verify-email/', views.verify_email, name='verify_email'),
    path('', include('dj_rest_auth.urls')),
    path('<str:user_id>/', views.user_info_update_delete, name="user_info_update_delete"),
]
