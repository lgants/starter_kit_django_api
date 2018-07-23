from graphene_django.views import GraphQLView
# from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view #, renderer_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import json
import os

@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
# @renderer_classes((JSONRenderer,))
def schema_view(request, format=None):
    print("ello", request.method)
    path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')
    with open(path , 'r') as file:
        data=file.read()

    # import pdb; pdb.set_trace()

    return Response(json.loads(data))


# @api_view(['GET'])
# def SchemaView(request, format=None):
#     from django.http import HttpResponse
#     path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')
#     return HttpResponse(open(path, 'r'), content_type='application/json; charset=utf8')



class BatchEnabledGraphQLView(GraphQLView):
    def __init__(self, **kwargs):
        kwargs.update({'batch':True})
        super(BatchEnabledGraphQLView, self).__init__(**kwargs)

    def get_response(self, request, data, show_graphiql=False):
        query, variables, operation_name, id = self.get_graphql_params(request, data)

        # if operation_name == 'IntrospectionQuery':
        #     path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')
        #     with open(path , 'r') as file:
        #         data=file.read()
        #     import pdb; pdb.set_trace()

        execution_result = self.execute_graphql_request(request, data, query, variables, operation_name, show_graphiql)

        status_code = 200

        if execution_result:
            print(execution_result.errors)
            print(execution_result.data)
            response = {}
            # import pdb; pdb.set_trace()

            if execution_result.errors:
                response['errors'] = [self.format_error(e) for e in execution_result.errors]

            if execution_result.invalid:
                status_code = 400
            else:
                response['data'] = execution_result.data

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None


        if operation_name == 'IntrospectionQuery':
            path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')
            with open(path , 'r') as file:
                data=file.read()

            return data, 200

        return result, status_code
