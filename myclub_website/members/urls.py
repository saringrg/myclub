from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name='authenticate/forgot_password.html', email_template_name='authenticate/password_reset_email.html'), name='forgot_password'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authenticate/password_reset_done.html'), name='password_reset_done'),    
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authenticate/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authenticate/password_reset_complete.html'), name='password_reset_complete'),
]

