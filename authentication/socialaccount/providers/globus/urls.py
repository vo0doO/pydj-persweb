from authentication.socialaccount.providers.globus.provider import GlobusProvider
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns


urlpatterns = default_urlpatterns(GlobusProvider)
