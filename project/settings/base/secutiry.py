# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: держите секретный ключ, используемый в производстве, в секрете!
# SECRET_KEY предоставляется через переменную окружения в OpenShift
# Безопасное значение, когда DJANGO_SECRET_KEY не может быть установлен
import os

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    # безопасное значение, используемое для разработки, когда DJANGO_SECRET_KEY не может быть установлен
    '9e4@&tw46$l31)zrqe3wi+-slqm(ruvz&se0^%9#6(_w3ui!c0'
)

ALLOWED_HOSTS = ['*']

# Проверка пароля
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
