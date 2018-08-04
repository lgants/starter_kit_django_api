"""starter_kit_django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
# from main.counters.views import MyView
from .views import BatchEnabledGraphQLView, NewGraphQLView, schema_view
from .NewViews import NewestGraphQLView, ModifiedGraphQLView
from .schema import schema
from ._views import MyGraphQLView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
    url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^schema', csrf_exempt(schema_view)),
    # url(r'^graphql', csrf_exempt(ModifiedGraphQLView.as_view(batch=True))),
    url(r'^graphql', csrf_exempt(MyGraphQLView.as_view(batch=True))),
    # url(r'^graphql', csrf_exempt(NewestGraphQLView.as_view(batch=True))),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(batch=True))),
    # url(r'^graphql', csrf_exempt(NewGraphQLView.as_view(batch=True))),
    # url(r'^graphql', csrf_exempt(BatchEnabledGraphQLView.as_view())),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# NOTE: this is not suitable for serving static files in production
