from django.db import models


class AccessInfo(models.Model):
    """Information needed to query API."""
    service = models.URLField()
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    expires_in = models.PositiveIntegerField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=500)
