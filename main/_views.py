from django.http import HttpResponse, HttpResponseNotAllowed
from graphene_django.views import GraphQLView, HttpError
import graphene
import json

class MyGraphQLView(GraphQLView):
    def __init__(self, **kwargs):
        super(MyGraphQLView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        request_type = request.META.get("CONTENT_TYPE", '')

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


    @staticmethod
    def get_graphql_params(request, data):
        request_type = request.META.get("CONTENT_TYPE", '')

        if "multipart/form-data" in request_type:
            query, variables, operation_name, id = super(MyGraphQLView, MyGraphQLView).get_graphql_params(request, data)
            operations = data.get('operations')
            files_map = data.get('map', "{}")

            try:
                operations = json.loads(operations)
                files_map = json.loads(files_map)

                variables = operations.get('variables')
                for file_key in files_map:
                    # file key is which file it is in the form-data
                    file_instances = files_map[file_key]
                    # pp.pprint(file_instances)
                    for file_instance in file_instances:
                        # print('file_instance')
                        # pp.pprint(file_instance)
                        test = obj_set(operations, file_instance, file_key, False)

                query = operations.get('query')
                variables = operations.get('variables')

            except Exception as e:
                raise e
                # raise HttpError(HttpResponseBadRequest('Operations are invalid JSON.'))

        else:
            query, variables, operation_name, id = super(MyGraphQLView, MyGraphQLView).get_graphql_params(request, data)

        return query, variables, operation_name, id

# class ObjectPath:
def getKey(key):
    try:
        intKey = int(key)
        return intKey
    except:
        return key

def getShallowProperty(obj, prop):
    if type(prop) is int:
        return obj[prop]

    try:
        return obj.get(prop)
    except:
        return None

def obj_set(obj, path, value, doNotReplace):
    if type(path) is int:
        path = [path]
    if path is None or len(path) == 0:
        return obj
    if isinstance(path, str):
        newPath = list(map(getKey, path.split('.')))
        return obj_set(obj, newPath, value, doNotReplace )

    currentPath = path[0]
    currentValue = getShallowProperty(obj, currentPath)

    if len(path) == 1:
        if currentValue is None or not doNotReplace:
            obj[currentPath] = value

    if currentValue is None:
        try:
            if type(path[1]) == int:
                obj[currentPath] = []
            else:
                obj[currentPath] = {}
        except Exception as e:
            pass
            # This line may need to be put back in but it will break it because it assumes an array.
            # obj[currentPath] = {}

    return obj_set(obj[currentPath], path[1:], value, doNotReplace)
