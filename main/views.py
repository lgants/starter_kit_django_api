from graphene_django.views import GraphQLView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os

@api_view()
def SchemaView(request):
    # import pdb; pdb.set_trace()
    path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')

    with open(path , 'r') as file:
        data=file.read()

    return Response(data)


class BatchEnabledGraphQLView(GraphQLView):
    def __init__(self, **kwargs):
        kwargs.update({'batch':True})
        super(BatchEnabledGraphQLView, self).__init__(**kwargs)

    def get_response(self, request, data, show_graphiql=False):
        query, variables, operation_name, id = self.get_graphql_params(request, data)

        execution_result = self.execute_graphql_request(request, data, query, variables, operation_name, show_graphiql)

        status_code = 200

        # import pdb; pdb.set_trace()
        # print(query)

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

            print("result", result)
        else:
            result = None

        return result, status_code
