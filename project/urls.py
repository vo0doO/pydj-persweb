from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import authentication.urls as auth_url
from project.apps.curiosity import urls as curiosity_urls
from welcome.views import health, index, readme

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', index),
    url(r'^readme$', readme),
    url(r'^health$', health),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^', include(auth_url)),
]

urlpatterns += [
    url(r'^curiosity/', include(curiosity_urls))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
