from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/send-email/', views.send_email, name='send_email'),
    path('signup/verify-email/', views.verify_email, name='verify_email'),
    path('signup/resend-email/', views.resend_email, name='resend_email'),
]
