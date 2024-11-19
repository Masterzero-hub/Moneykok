from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('signup/send-code-email/', views.send_code_email, name='send_code_email'),
    path('signup/verify-email/', views.verify_email, name='verify_email'),
    path('signup/resend-code-email/', views.resend_code_email, name='resend_code_email'),
]
