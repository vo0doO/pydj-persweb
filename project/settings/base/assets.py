# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
import os

from django.conf import settings

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
