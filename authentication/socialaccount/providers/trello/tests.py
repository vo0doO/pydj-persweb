# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from authentication.socialaccount.tests import OAuthTestsMixin
from authentication.tests import TestCase

from .provider import TrelloProvider


class TrelloTests(OAuthTestsMixin, TestCase):
    provider_id = TrelloProvider.id
