from django.conf import settings

# чтобы позволить клиенту апи сохранить состояние окружающей среды в базу данных.
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# мы используем cached_db бэкенд для longlive и быстрых сессий.
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_NAME = 'sid'
SESSION_COOKIE_AGE = 86400 * 60  # 2 месяца. Очень важно помнить пользователя.

if settings.PRODUCTION:
    SESSION_COOKIE_DOMAIN = '.имя производственного хоста с точкой (RFC)'
