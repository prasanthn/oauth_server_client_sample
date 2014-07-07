from django import forms

from . import models


class AuthorizeForm(forms.Form):
    pass


class AppRegistrationForm(forms.ModelForm):
    """Form for registering app.

    Before saving make sure to set owner (current user), client, and client's
    properites.
    """
    redirect_uri = forms.URLField()

    class Meta:
        model = models.App
        fields = ('name', 'description', 'iframe_url')
