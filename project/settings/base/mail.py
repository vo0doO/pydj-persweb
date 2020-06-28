import os

from django.conf import settings

from project.conf.mail import mail

# SERVER_EMAIL = ''
# DEFAULT_FROM_EMAIL = ''
ADMINS = (('Danila Kirsanov', 'exenoobe@gmail.com'),)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER=mail.us()
EMAIL_HOST_PASSWORD = mail.pa()
EMAIL_USE_TLS = True
