This repo contains two Django projects.

The first project "oauth2_server" implements an OAuth2 server, using oauth2app,
and has an API serivce that allows approved clients access to user's data.

The second project "oauth2_client" is a client, that has registered with the
server. It will ask a user to approve it and then will query the server for some
of the user's data stored on it.


----

Scopes are asked for in each approval. That is scopes are associated with an
AccessKey and not the app itself. Each approval request must list the scopes the
app wants from the user. Each API request must also list the scopes; these must
be a subset of the scopes associated with the request's AccessKey.

----
