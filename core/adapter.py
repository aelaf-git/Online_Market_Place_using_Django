from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        # If the user doesn't have a profile picture, redirect them to setup
        if not hasattr(user, 'profile') or not user.profile.image:
            return reverse('core:setup_profile')
        return super().get_login_redirect_url(request)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        # If the user logged in via Google and has no profile picture, redirect to setup
        if not hasattr(user, 'profile') or not user.profile.image:
            return reverse('core:setup_profile')
        return super().get_login_redirect_url(request)
