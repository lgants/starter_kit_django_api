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
# from main.counters.views import MyView

class BatchEnabledGraphQLView(GraphQLView):
	"""
	Modified graphql view that enables batched queries
	"""

	def __init__(self, **kwargs):
		kwargs.update({'batch':True})
		super(BatchEnabledGraphQLView, self).__init__(**kwargs)

	def get_response(self, request, data, show_graphiql=False):
		import pdb; pdb.set_trace()



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
    # url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(batch=True))),
    url(r'^graphql', csrf_exempt(BatchEnabledGraphQLView.as_view())),
]
