from graphene_django.views import GraphQLView

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
            print(query)
            response = {}

            if execution_result.errors:
                response['errors'] = [self.format_error(e) for e in execution_result.errors]

            if execution_result.invalid:
                status_code = 400
            else:
                response['data'] = execution_result.data

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None

        return result, status_code
