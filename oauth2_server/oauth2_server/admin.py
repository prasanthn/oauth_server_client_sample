from django.contrib import admin

from oauth2app.oauth2app import models as o2amodels
from . import models

admin.site.register(o2amodels.Client)
admin.site.register(o2amodels.AccessRange)
admin.site.register(o2amodels.AccessToken)
admin.site.register(o2amodels.Code)
admin.site.register(o2amodels.MACNonce)

admin.site.register(models.App)
