from authentication.socialaccount.providers.jupyterhub.provider import (
    JupyterHubProvider,
)
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns


urlpatterns = default_urlpatterns(JupyterHubProvider)
