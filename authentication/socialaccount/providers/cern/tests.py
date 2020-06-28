from authentication.socialaccount.tests import OAuth2TestsMixin
from authentication.tests import MockedResponse, TestCase

from .provider import CernProvider


class CernTests(OAuth2TestsMixin, TestCase):
    provider_id = CernProvider.id

    def get_mocked_response(self):
        return MockedResponse(200, """
        {
            "name":"Max Mustermann",
            "username":"mmuster",
            "id":8173921,
            "personid":924225,
            "email":"max.mustermann@cern.ch",
            "first_name":"Max",
            "last_name":"Mustermann",
            "identityclass":"CERN Registered",
            "federation":"CERN",
            "phone":null,
            "mobile":null
        }
        """)
