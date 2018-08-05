from graphene_django.views import GraphQLView
# from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view #, renderer_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
# from django.http import HttpResponse, HttpResponseNotAllowed
# from graphene_django.views import GraphQLView, HttpError
# import graphene
# import json
import graphene
import json
import os

@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
# @renderer_classes((JSONRenderer,))
def schema_view(request, format=None):
    # print("ello", request.method)
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
        # import pdb; pdb.set_trace()

        execution_result = self.execute_graphql_request(request, data, query, variables, operation_name, show_graphiql)

        status_code = 200

        if execution_result:
            # print(execution_result.errors)
            # print(execution_result.data)
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


        if operation_name == 'IntrospectionQuery':
            path = os.path.join(settings.BASE_DIR, 'main/static/schema.json')
            with open(path , 'r') as file:
                data=file.read()

            return data, 200

        return result, status_code


class NewGraphQLView(GraphQLView):
    def __init__(self, **kwargs):
        # kwargs.update({'batch':True})
        super(NewGraphQLView, self).__init__(**kwargs)

    # @staticmethod
    # def get_graphql_params(request, data):
    #     request_type = request.META.get("CONTENT_TYPE", '')
    #
    #     if "multipart/form-data" in request_type:
    #         import pdb; pdb.set_trace()

    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         if request.method.lower() not in ("get", "post"):
    #             raise HttpError(
    #                 HttpResponseNotAllowed(
    #                     ["GET", "POST"], "GraphQL only supports GET and POST requests."
    #                 )
    #             )
    #
    #         data = self.parse_body(request)
    #         show_graphiql = self.graphiql and self.can_display_graphiql(request, data)
    #
    #         if "multipart/form-data" in request_type:
    #             import pdb; pdb.set_trace()
    #
    #         if self.batch:
    #             responses = [self.get_response(request, entry) for entry in data]
    #             result = "[{}]".format(
    #                 ",".join([response[0] for response in responses])
    #             )
    #             status_code = (
    #                 responses
    #                 and max(responses, key=lambda response: response[1])[1]
    #                 or 200
    #             )
    #         else:
    #             result, status_code = self.get_response(request, data, show_graphiql)
    #
    #         if show_graphiql:
    #             query, variables, operation_name, id = self.get_graphql_params(
    #                 request, data
    #             )
    #             return self.render_graphiql(
    #                 request,
    #                 graphiql_version=self.graphiql_version,
    #                 query=query or "",
    #                 variables=json.dumps(variables) or "",
    #                 operation_name=operation_name or "",
    #                 result=result or "",
    #             )
    #
    #         return HttpResponse(
    #             status=status_code, content=result, content_type="application/json"
    #         )
    #
    #     except HttpError as e:
    #         response = e.response
    #         response["Content-Type"] = "application/json"
    #         response.content = self.json_encode(
    #             request, {"errors": [self.format_error(e)]}
    #         )
    #         return response

    # def get_response(self, request, data, show_graphiql=False):
    #     query, variables, operation_name, id = self.get_graphql_params(request, data)
    #
    #     request_type = request.META.get("CONTENT_TYPE", '')
    #
    #     if "multipart/form-data" in request_type:
    #         import pdb; pdb.set_trace()
    #
    #
    #     execution_result = self.execute_graphql_request(
    #         request, data, query, variables, operation_name, show_graphiql
    #     )
    #
    #     status_code = 200
    #     if execution_result:
    #         response = {}
    #
    #         if execution_result.errors:
    #             response["errors"] = [
    #                 self.format_error(e) for e in execution_result.errors
    #             ]
    #
    #         if execution_result.invalid:
    #             status_code = 400
    #         else:
    #             response["data"] = execution_result.data
    #
    #         if self.batch:
    #             response["id"] = id
    #             response["status"] = status_code
    #
    #         result = self.json_encode(request, response, pretty=show_graphiql)
    #     else:
    #         result = None
    #
    #     return result, status_code

    def parse_body(self, request):
        content_type = self.get_content_type(request)

        if content_type == "application/graphql":
            return {"query": request.body.decode()}

        elif content_type == "application/json":
            # noinspection PyBroadException
            try:
                body = request.body.decode("utf-8")
            except Exception as e:
                raise HttpError(HttpResponseBadRequest(str(e)))

            try:
                request_json = json.loads(body)
                if self.batch:
                    assert isinstance(request_json, list), (
                        "Batch requests should receive a list, but received {}."
                    ).format(repr(request_json))
                    assert (
                        len(request_json) > 0
                    ), "Received an empty list in the batch request."
                else:
                    assert isinstance(
                        request_json, dict
                    ), "The received data is not a valid JSON query."
                return request_json
            except AssertionError as e:
                raise HttpError(HttpResponseBadRequest(str(e)))
            except (TypeError, ValueError):
                raise HttpError(HttpResponseBadRequest("POST body sent invalid JSON."))

        elif content_type in [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ]:
            # import pdb; pdb.set_trace()
            request_json = json.loads(body)
            body = request.POST.get('operations')
            return request.POST

        return {}


class ModifiedGraphQLView(GraphQLView):
    # graphiql_template = 'graphiql.html'
    # import pdb; pdb.set_trace()

    # @staticmethod
    # def get_graphql_params(request, data):
    #     # print("data", data['operationName'])
    #     request_type = request.META.get("CONTENT_TYPE", '')
    #     # import pdb; pdb.set_trace()
    #
    #     print("request_type", request_type)
    #     print("request", request)
    #     # print("request._post", request._post)
    #     print("data", data)
    #
    #     if "multipart/form-data" in request_type:
    #         _data = json.loads(request._post.get("operations"))
    #
    #         query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, _data)
    #         # operations = data.get('operations')
    #         # files_map = data.get('map', "{}")
    #
    #         # import pdb; pdb.set_trace()
    #         operations = request._post.get("operations")
    #         files_map = request._post.get("map", "{}")
    #
    #
    #         try:
    #             operations = json.loads(operations)
    #             files_map = json.loads(files_map)
    #
    #             variables = operations.get('variables')
    #             for file_key in files_map:
    #                 # file key is which file it is in the form-data
    #                 file_instances = files_map[file_key]
    #                 # pp.pprint(file_instances)
    #                 for file_instance in file_instances:
    #                     # print('file_instance')
    #                     # pp.pprint(file_instance)
    #                     test = obj_set(operations, file_instance, file_key, False)
    #
    #             query = operations.get('query')
    #             variables = operations.get('variables')
    #
    #         except Exception as e:
    #             raise e
    #             # raise HttpError(HttpResponseBadRequest('Operations are invalid JSON.'))
    #
    #     else:
    #         query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, data)
    #
    #
    #     # Example Request Body
    #     # {'map': '{"0":["variables.file"]}',
    #     #  'operations': '{"query":"mutation ($file: Upload!) {\\n  '
    #     #                'uploadImageTest(file: $file) {\\n    success\\n    '
    #     #                '__typename\\n  }\\n}\\n","variables":{}}'}
    #     #
    #     # Need to maybe map the map into the variables for files so that way the
    #     # resolver knows which file on the multipart form to access
    #     # import pdb; pdb.set_trace()
    #
    #
    #     return query, variables, operation_name, id
    @staticmethod
    def get_graphql_params(request, data):
        request_type = request.META.get("CONTENT_TYPE", '')

        if "multipart/form-data" in request_type:
            _data = json.loads(request._post.get("operations"))

            query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, _data)
            operations = request._post.get('operations')
            files_map = request._post.get('map', "{}")

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

            return query, variables, operation_name, id
        else:
            query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, data)

        # Example Request Body
        # {'map': '{"0":["variables.file"]}',
        #  'operations': '{"query":"mutation ($file: Upload!) {\\n  '
        #                'uploadImageTest(file: $file) {\\n    success\\n    '
        #                '__typename\\n  }\\n}\\n","variables":{}}'}
        #
        # Need to maybe map the map into the variables for files so that way the
        # resolver knows which file on the multipart form to access


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


# # NOTE: this works so leaving for reference, but will use the package
# class MyGraphQLView(GraphQLView):
#     def __init__(self, **kwargs):
#         super(MyGraphQLView, self).__init__(**kwargs)
#
#     def dispatch(self, request, *args, **kwargs):
#         request_type = request.META.get("CONTENT_TYPE", '')
#
#         if "multipart/form-data" in request_type:
#             try:
#                 if request.method.lower() not in ("get", "post"):
#                     raise HttpError(
#                         HttpResponseNotAllowed(
#                             ["GET", "POST"], "GraphQL only supports GET and POST requests."
#                         )
#                     )
#
#                 data = self.parse_body(request)
#                 show_graphiql = self.graphiql and self.can_display_graphiql(request, data)
#
#                 result, status_code = self.get_response(request, data, show_graphiql)
#
#                 if show_graphiql:
#                     query, variables, operation_name, id = self.get_graphql_params(
#                         request, data
#                     )
#
#                     return self.render_graphiql(
#                         request,
#                         graphiql_version=self.graphiql_version,
#                         query=query or "",
#                         variables=json.dumps(variables) or "",
#                         operation_name=operation_name or "",
#                         result=result or "",
#                     )
#
#                 return HttpResponse(
#                     status=status_code, content=result, content_type="application/json"
#                 )
#
#             except HttpError as e:
#                 response = e.response
#                 response["Content-Type"] = "application/json"
#                 response.content = self.json_encode(
#                     request, {"errors": [self.format_error(e)]}
#                 )
#                 return response
#
#         else:
#             return super(MyGraphQLView, MyGraphQLView).dispatch(self, request, *args, **kwargs)
#
#
#     @staticmethod
#     def get_graphql_params(request, data):
#         request_type = request.META.get("CONTENT_TYPE", '')
#
#         if "multipart/form-data" in request_type:
#             query, variables, operation_name, id = super(MyGraphQLView, MyGraphQLView).get_graphql_params(request, data)
#             operations = data.get('operations')
#             files_map = data.get('map', "{}")
#
#             try:
#                 operations = json.loads(operations)
#                 files_map = json.loads(files_map)
#
#                 variables = operations.get('variables')
#                 for file_key in files_map:
#                     # file key is which file it is in the form-data
#                     file_instances = files_map[file_key]
#                     # pp.pprint(file_instances)
#                     for file_instance in file_instances:
#                         # print('file_instance')
#                         # pp.pprint(file_instance)
#                         test = obj_set(operations, file_instance, file_key, False)
#
#                 query = operations.get('query')
#                 variables = operations.get('variables')
#
#             except Exception as e:
#                 raise e
#                 # raise HttpError(HttpResponseBadRequest('Operations are invalid JSON.'))
#
#         else:
#             query, variables, operation_name, id = super(MyGraphQLView, MyGraphQLView).get_graphql_params(request, data)
#
#         return query, variables, operation_name, id
#
# # class ObjectPath:
# def getKey(key):
#     try:
#         intKey = int(key)
#         return intKey
#     except:
#         return key
#
# def getShallowProperty(obj, prop):
#     if type(prop) is int:
#         return obj[prop]
#
#     try:
#         return obj.get(prop)
#     except:
#         return None
#
# def obj_set(obj, path, value, doNotReplace):
#     if type(path) is int:
#         path = [path]
#     if path is None or len(path) == 0:
#         return obj
#     if isinstance(path, str):
#         newPath = list(map(getKey, path.split('.')))
#         return obj_set(obj, newPath, value, doNotReplace )
#
#     currentPath = path[0]
#     currentValue = getShallowProperty(obj, currentPath)
#
#     if len(path) == 1:
#         if currentValue is None or not doNotReplace:
#             obj[currentPath] = value
#
#     if currentValue is None:
#         try:
#             if type(path[1]) == int:
#                 obj[currentPath] = []
#             else:
#                 obj[currentPath] = {}
#         except Exception as e:
#             pass
#             # This line may need to be put back in but it will break it because it assumes an array.
#             # obj[currentPath] = {}
#
#     return obj_set(obj[currentPath], path[1:], value, doNotReplace)
