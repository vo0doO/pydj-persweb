from authentication.socialaccount.providers.base import ProviderAccount
from authentication.socialaccount.providers.oauth2.provider import OAuth2Provider


class TwitchAccount(ProviderAccount):
    def get_profile_url(self):
        return 'http://twitch.tv/' + self.account.extra_data.get('name')

    def get_avatar_url(self):
        return self.account.extra_data.get('logo')

    def to_str(self):
        dflt = super(TwitchAccount, self).to_str()
        return self.account.extra_data.get('name', dflt)


class TwitchProvider(OAuth2Provider):
    id = 'twitch'
    name = 'Twitch'
    account_class = TwitchAccount

    def extract_uid(self, data):
        return str(data['_id'])

    def extract_common_fields(self, data):
        return {
            "username": data.get("name"),
            "name": data.get("display_name"),
            "email": data.get("email"),
        }

    def get_default_scope(self):
        return ["user_read"]


provider_classes = [TwitchProvider]
