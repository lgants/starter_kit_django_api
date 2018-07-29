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
from django.conf.urls import url
from django.contrib import admin
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
# from main.counters.views import MyView
from .views import BatchEnabledGraphQLView, ModifiedGraphQLView, schema_view
from .schema import schema

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
    url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^schema', csrf_exempt(schema_view)),
    url(r'^graphql', csrf_exempt(ModifiedGraphQLView.as_view(batch=True))),
    url(r'^', TemplateView.as_view(template_name="index.html")),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(batch=True))),
    # url(r'^graphql', csrf_exempt(BatchEnabledGraphQLView.as_view())),
]
