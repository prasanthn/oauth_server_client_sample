from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'oauth2_server',
    # Examples:
    # url(r'^$', 'oauth2_server.views.home', name='home'),
    # url(r'^oauth2_server/', include('oauth2_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'views.front', name='front'),
    url(r'^register-app/$', 'views.register_app', name='register_app'),
    url(r'^register-app-success/$', 'views.register_app_success',
        name='register_app_success'),
    url(r'^app/(?P<app_id>\w+)/?$', 'views.app', name='app'),
    url(r'^install-app/$', 'views.install_app', name='install_app'),
    url(r'^revoke-app/(?P<app_id>\w+)/?$', 'views.revoke_app', name='revoke_app')

)

# OAuth2App
urlpatterns += patterns(
    '',
    (r'^oauth2/missing_redirect_uri/?$', 'oauth2_server.views.missing_redirect_uri'),
    (r'^oauth2/authorize/?$', 'oauth2_server.views.authorize'),
    (r'^oauth2/authorize-code/?$', 'oauth2_server.views.authorize_code'),
    (r'^oauth2/token/?$', 'oauth2app.oauth2app.token.handler'),
)

urlpatterns += patterns(
    '',
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', name='logout'),
)

urlpatterns += patterns(
    'oauth2_server',
    url(r'^api/username/?$', 'api.username', name="api_username")
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
