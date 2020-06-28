# -*- coding: utf-8 -*-
from authentication.socialaccount.providers.gitlab.provider import GitLabProvider
from authentication.socialaccount.providers.oauth2.urls import default_urlpatterns


urlpatterns = default_urlpatterns(GitLabProvider)
