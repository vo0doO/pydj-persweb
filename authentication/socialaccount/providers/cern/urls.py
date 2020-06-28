from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import CernProvider


urlpatterns = default_urlpatterns(CernProvider)
