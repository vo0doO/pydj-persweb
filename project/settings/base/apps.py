# Определение приложений

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.redirects',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.syndication',

    'crispy_forms',
    
    'authentication',
    'authentication.account',
    'authentication.socialaccount',
    'welcome',

    'project.apps.curiosity',
]
