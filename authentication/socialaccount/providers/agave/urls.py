from authentication.socialaccount.providers.agave.provider import AgaveProvider
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns


urlpatterns = default_urlpatterns(AgaveProvider)
