from django.urls import path
from . import views
from .forms import EmailOrUsernameAuthenticationForm
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view( # la LoginView viene impostata in settings.py
        template_name='accounts/login.html',
        authentication_form=EmailOrUsernameAuthenticationForm,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm')
]
