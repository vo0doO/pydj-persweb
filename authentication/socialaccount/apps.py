from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SocialAccountConfig(AppConfig):
    name = 'authentication.socialaccount'
    verbose_name = _('Social Accounts')
