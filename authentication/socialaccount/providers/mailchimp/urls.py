"""Register urls for MailChimpProvider"""
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import MailChimpProvider


urlpatterns = default_urlpatterns(MailChimpProvider)
