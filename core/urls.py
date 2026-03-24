from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, SignupForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-code/', views.resend_verification_code, name='resend_code'),
    path('setup-profile/', views.setup_profile, name='setup_profile'),
    path('settings/', views.settings, name='settings'),
]