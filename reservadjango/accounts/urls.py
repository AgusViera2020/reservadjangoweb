from django.urls import path
from .views import SignUpView, login_view, email_check, PasswordsChangeView, pass_success, update_user,update_user_info
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name = "signup"),
    path("login/", login_view, name = "login"),

    path("update_user/", update_user, name = "update_user"),
    path("user_info/", update_user_info, name = "update_user_info"),
    
    path("email_check/", email_check, name = "email_check"),
    
    path('password_change/', PasswordsChangeView.as_view(template_name='registration/password_change.html')),
    path('password_change/done/', pass_success),
    

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset.html'), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_complete"),
    ]