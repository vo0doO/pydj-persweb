from authentication.socialaccount.providers import registry
from authentication.socialaccount.tests import create_oauth2_tests
from authentication.tests import MockedResponse

from .provider import RobinhoodProvider


class RobinhoodTests(create_oauth2_tests(
        registry.by_id(RobinhoodProvider.id))):

    def get_mocked_response(self):
        return MockedResponse(200, """
{
  "username": "test_username",
  "id": "1234-5678-910"
}
        """)
