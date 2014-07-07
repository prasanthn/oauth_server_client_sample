from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'oauth2_client',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'views.front', name='front'),
    url(r'^redirect-uri/?$', 'views.redirect_uri', name='redirect_uri'),
    url(r'^redirect-uri-code/?$', 'views.redirect_uri_code', name='redirect_uri_code'),
    url(r'^iframe-url/?$', 'views.iframe_url', name='iframe_url')
)


# Use Django to serve media and static files --- even when DEBUG == False. In
# production environment configure server to serve from these URLs so that the
# request never reaches Django. Heroku's Python example project repo recommends
# these settings, along with gunicorn as server.
from django.conf import settings
static_url = settings.STATIC_URL.lstrip('/').rstrip('/')
urlpatterns += patterns(
    '',
    (r'^%s/(?P<path>.*)$' % static_url, 'django.views.static.serve',
     {
         'document_root': settings.STATIC_ROOT,
     }),
)
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
urlpatterns += patterns(
    '',
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT,
        }),
)
