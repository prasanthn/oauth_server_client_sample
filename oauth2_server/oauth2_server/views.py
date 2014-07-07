from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from oauth2app.oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.oauth2app.models import Client
from oauth2app.oauth2app.consts import TOKEN, CODE

from . import models
from . import forms


def front(request):
    """List all clients in the front page."""
    apps = models.App.objects.all().select_related()
    installed_apps = []
    if request.user.is_authenticated():
        installed_apps = [a.client.app for a in request.user.accesstoken_set.all().prefetch_related()]

    return render(request, "front.html", {'apps': apps, 'installed_apps': installed_apps})


@login_required
def app(request, app_id):
    """Display details of an app."""
    app = get_object_or_404(models.App, pk=app_id)
    installed = False
    if app.client.accesstoken_set.filter(user__username='super').exists():
        installed = True

    return render(request, "app.html", {'app': app, 'installed': installed})


@login_required
def register_app(request):
    if request.method == 'GET':
        return render(request, "register_app.html",
                      {'form': forms.AppRegistrationForm()})
    if request.method == 'POST':
        form = forms.AppRegistrationForm(data=request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            app.client = Client.objects.create(
                name=app.name, user=app.owner,
                description=app.description,
                redirect_uri=form.cleaned_data['redirect_uri'])
            app.save()
            request.session['register_app_success'] = app.id
            return redirect(reverse("register_app_success"))
        else:
            return render(request, "register_app.html",
                          {'form': form})


@login_required
def register_app_success(request):
    app_id = request.session.get('register_app_success', None)
    if app_id:
        del request.session['register_app_success']
        app = models.App.objects.get(pk=app_id)

        return render(request, "register_app_success.html",
                      {'app': app})
    else:
        return HttpResponseNotFound()


@login_required
def install_app(request):
    apps = set(models.App.objects.all().select_related())
    installed_apps = set([a.client.app for a in request.user.accesstoken_set.all().prefetch_related()])
    apps = apps - installed_apps
    return render(request, 'install_app.html', {'apps': apps})


@login_required
def authorize(request):

    authorizer = Authorizer(response_type=TOKEN)  # allow direct creation of token
    try:
        authorizer.validate(request)
    except MissingRedirectURI:
        return redirect("/oauth2/missing_redirect_uri")
    except AuthorizationException:
        # The request is malformed or invalid. Automatically
        # redirects to the provided redirect URL.

        # The OAuth2App likes to redirect to redirect_uri but in our case
        # AuthorizationException should never happen since we create the link
        # that leads a user to this view. So we should log this and make note
        # that an malformed request has been made.
        # return authorizer.error_redirect()
        return HttpResponseBadRequest()

    if request.method == 'GET':
        data = {
            "client": authorizer.client,
            "app": authorizer.client.app,
            "access_ranges": authorizer.access_ranges,
            "action": '/oauth2/authorize?%s' % authorizer.query_string,
            "method": 'POST'
        }
        return render(request, 'authorize.html', data)

    elif request.method == 'POST':
        if request.POST.get("connect") == "Yes":
            return authorizer.grant_redirect()
        else:
            # The OAuth2App likes to redirect to redirect_uri but
            # we will simply intercept the request and send user back to
            # home page
            # return authorizer.error_redirect()
            return redirect(reverse("front"))

    return redirect(reverse("front"))


@login_required
def authorize_code(request):

    authorizer = Authorizer(response_type=CODE)
    try:
        authorizer.validate(request)
    except MissingRedirectURI:
        return redirect("/oauth2/missing_redirect_uri")
    except AuthorizationException:
        # The request is malformed or invalid. Automatically
        # redirects to the provided redirect URL.

        # The OAuth2App likes to redirect to redirect_uri but in our case
        # AuthorizationException should never happen since we create the link
        # that leads a user to this view. So we should log this and make note
        # that an malformed request has been made.
        # return authorizer.error_redirect()
        return HttpResponseBadRequest()

    if request.method == 'GET':
        data = {
            "client": authorizer.client,
            "app": authorizer.client.app,
            "access_ranges": authorizer.access_ranges,
            "action": '/oauth2/authorize-code?%s' % authorizer.query_string,
            "method": 'POST'
        }
        return render(request, 'authorize.html', data)

    elif request.method == 'POST':
        if request.POST.get("connect") == "Yes":
            return authorizer.grant_redirect()
        else:
            # The OAuth2App likes to redirect to redirect_uri but
            # we will simply intercept the request and send user back to
            # home page
            # return authorizer.error_redirect()
            return redirect(reverse("front"))

    return redirect(reverse("front"))


@login_required
def revoke_app(request, app_id):
    app = get_object_or_404(models.App, pk=app_id)
    if not app.client.accesstoken_set.filter(user=request.user).exists():
        return redirect(reverse('front'))

    if request.method == 'GET':
        return render(request, 'revoke_app.html', {'app': app})
    elif request.method == 'POST':
        if request.POST.get('consent') == 'Yes':
            access_token = app.client.accesstoken_set.get(user=request.user)
            access_token.delete()
            return redirect(reverse('front'))


def missing_redirect_uri(request):
    pass
