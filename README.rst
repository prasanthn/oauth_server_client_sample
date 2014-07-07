This repo contains two Django projects.

The first project "oauth2_server" implements an OAuth2 server, using oauth2app,
and has an API serivce that allows approved clients access to user's data.

The second project "oauth2_client" is a client, that has registered Apps with
the server. When a user on oauth2_server installs an App, the server will notify
the client and then the client will query the server for some of the user's data
stored on it.

----

Scopes are asked for in each approval. That is scopes are associated with an
AccessKey and not the app itself. Each approval request must list the scopes the
app wants from the user. Each API request must also list the scopes; these must
be a subset(?) of the scopes associated with the request's AccessKey.

----

Registering an app creates an App instance as well as a Client instance:
OneToOne from App to Client.

----

Installing app.

First apps must be registered. During this process the App is given a client_id
and client_key.

There are two OAuth methods for granting access to apps. One method, called CODE
is used if the app is running on its own server. Second, called TOKEN, if the
app is running in a browser; of-course the first kind of app can use this method
also. The names are my creation for easy reference and not something you will
find in OAuth literature.

In the sample app I have setup both.

In both methods the user, on our server (oauth2_server in the sample app) clicks
on "an install button". The user is taken to a confirmation page, where they
will be shown information regarding the app, the permissions required by the
app, and asks the user to give yes or no consent. If the user selects "No" then
the process is aborted. If the user selects "Yes" then the following happens;
the steps are different in CODE and TOKEN methods.

In the CODE method, a request is send (via browser redirect) to the redirect_uri
registered by the App (redirect_uri_code view in oauth2_client in sample app).
This request will contain an authorisation_code. The server hosting the App must
then send a server-to-server request passing along the authorisation code,
client id and client secret (the app obtains the last two while registering the
app). The OAuth server will check that the data is valid, and if so will send
back the access token. This process is called exchanging the code. Notice that
the user is still sitting in the redirect_uri page while the App exchanges the
code for the token. After receiving the token the server running the App can
display a message and redirect back to our server (say the apps page) or simply
display a welcome message or take them to their own "accounts" page.

In the TOKEN method the OAuth server creates the token when user clicks "Yes",
and then redirect user to redirect_uri passing along access_token and other
information. This information is passed along as URL fragments and not as GET
parameters. The App must have JavaScript code at redirect_uri that processes
this information, and then can store the information if needed, and so on. They
then can choose to redirect to our server or display their UI and so on.


Access tokens have an expiration time. In the sample app the expiration time is
set to 20 years i.e., the acess token is for life.


While requesting info using the API Apps must pass along the access token that
they were given using the Authorization header.

I haven't written a full App but App1 in the code can do the equivalent of the
following:

    res = req.get("http://127.0.0.1:8000/api/username",
                  headers={'Authorization': 'Bearer 429dbad69a'})
    res.content
    '{"username": "super"}'


And App2 can do the following:

    res = req.get("http://127.0.0.1:8000/api/username",
                  headers={'Authorization': 'Bearer fdeaa1efe0'})

    res.content
    '{"username": "super"}'


----

Sample app

1. Run oauth2_server/manage.py runserver 8000 (OAuth server)
2. Run oauth2_client/manage.py runserver 8010 (OAuth app)
3. I have included the sqlite database file in the repo and hence user accounts
   and apps should be already setup. App2 wants CODE method and App1
   wants TOKEN method.
4. Go to server front page and click on "register app", "install app" and so on.

-----

A draft design plan

+  Page for "developers" to register their apps. The App must have
   a redirect_uri for exchanging OAuth information, scopes (i.e., permissions),
   and an iframe_url which will be the URL of the actual app.
+  A section in the dashboard that lists all registered apps available for use
   by the current user.
+  User click on app after choosing which company the app is to be added to.
   This is the "Install app" action.
+  A page is displayed showing details of the App, inlcuding the permissions it
   requires. User can now click on "Yes" or "No".
+  Clicking "No" takes user back to app list. Clicking "Yes" initiates the
   CODE method.
+  An authorization code is created, user is redirected to redirect_uri. While the
   user stays at redirect_uri, the app sends a server-to-server request asking for access token. We supply the access token. App server then displays some information or not, and then redirects to our site.
+  User can click on "open app". This embeds the iframe_url in the dashboard so that
   the user see the app within our site.
