# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from authentication.socialaccount.providers import registry
from authentication.socialaccount.tests import create_oauth2_tests
from authentication.tests import MockedResponse

from .provider import RedditProvider


class RedditTests(create_oauth2_tests(registry.by_id(
        RedditProvider.id))):
    def get_mocked_response(self):
        return [MockedResponse(200, """{
        "name": "wayward710"}""")]
