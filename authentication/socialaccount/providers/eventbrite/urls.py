"""Register urls for EventbriteProvider"""
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import EventbriteProvider


urlpatterns = default_urlpatterns(EventbriteProvider)
