from authentication.socialaccount.providers.discord.provider import DiscordProvider
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns


urlpatterns = default_urlpatterns(DiscordProvider)
