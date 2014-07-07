from django.db import models
from django.contrib.auth import get_user_model

from oauth2app.oauth2app.models import Client

AUTH_USER_MODEL = get_user_model()


class App(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='owned_apps')
    client = models.OneToOneField(Client, related_name='app')
    iframe_url = models.URLField()
    response_type = models.CharField(max_length=25)

    @property
    def secret(self):
        return self.client.secret

    @property
    def key(self):
        return self.client.key

    @property
    def redirect_uri(self):
        return self.client.redirect_uri

    def __unicode__(self):
        return self.name
