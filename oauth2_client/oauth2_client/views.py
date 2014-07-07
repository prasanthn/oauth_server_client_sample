import requests as req
import json

from django.shortcuts import render

from . import models


def redirect_uri(request):
    return render(request, 'welcome_token.html')


def redirect_uri_code(request):
    """Exchange code for access token."""
    code = request.GET.get('code', None)
    if code:
        res = req.post(
            "http://127.0.0.1:8000/oauth2/token",
            {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'http://127.0.0.1:8010/redirect-uri-code',
                'client_id': '10d00997deb47af570938c2ffcda61',
                'client_secret': 'ed97798e2c42b8e908579ecd9cc5a2'
            }
        )
        data = json.loads(res.content)
        if not data.get('error'):
            models.AccessInfo.objects.create(
                service="http://127.0.0.1:8000",
                access_token=data['access_token'],
                token_type=data['token_type'],
                expires_in=data['expires_in'],
                refresh_token=data['refresh_token'],
                scope=data['scope']
            )

    return render(request, "welcome.html", {'data': data})
