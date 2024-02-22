from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url

class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        assert request.user.is_authenticated
        if (request.user.profile_complete):
            url = settings.LOGIN_REDIRECT_URL
        else:
            url = '/accounts/edit_profile'
        return resolve_url(url)