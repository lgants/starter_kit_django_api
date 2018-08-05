from graphene_django.views import GraphQLView, HttpError
from django.http import HttpResponse, HttpResponseNotAllowed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from graphene_file_upload import ModifiedGraphQLView
import graphene
import json
import os

@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def schema_view(request, format=None):
    path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')
    with open(path , 'r') as file:
        data=file.read()
    return Response(json.loads(data))



# NOTE: this works so leaving for reference, but will use the package
class MyGraphQLView(ModifiedGraphQLView):
    def __init__(self, **kwargs):
        super(MyGraphQLView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        request_type = request.META.get("CONTENT_TYPE", '')

        # NOTE: need to overwrite inherited dispatch func and handle explicitly if multipart since batch=True incorrectly treats multipart as a batch request
        if "multipart/form-data" in request_type:
            try:
                if request.method.lower() not in ("get", "post"):
                    raise HttpError(
                        HttpResponseNotAllowed(
                            ["GET", "POST"], "GraphQL only supports GET and POST requests."
                        )
                    )

                data = self.parse_body(request)
                show_graphiql = self.graphiql and self.can_display_graphiql(request, data)

                result, status_code = self.get_response(request, data, show_graphiql)

                if show_graphiql:
                    query, variables, operation_name, id = self.get_graphql_params(
                        request, data
                    )

                    return self.render_graphiql(
                        request,
                        graphiql_version=self.graphiql_version,
                        query=query or "",
                        variables=json.dumps(variables) or "",
                        operation_name=operation_name or "",
                        result=result or "",
                    )

                return HttpResponse(
                    status=status_code, content=result, content_type="application/json"
                )

            except HttpError as e:
                response = e.response
                response["Content-Type"] = "application/json"
                response.content = self.json_encode(
                    request, {"errors": [self.format_error(e)]}
                )
                return response

        else:
            return super(MyGraphQLView, MyGraphQLView).dispatch(self, request, *args, **kwargs)
