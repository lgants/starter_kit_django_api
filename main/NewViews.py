from graphene_django.views import GraphQLView
import json
import graphene

# Implement this spec:
# https://github.com/jaydenseric/graphql-multipart-request-spec

# "Multipart GraphQL server requests are handled by apollo-upload-server middleware.
# The files upload to a temp directory, the operations field is JSON decoded and object-path
# is used to insert metadata about each of the uploads (including the temp path) in place of
# the original files in the resolver arguments."

# Basically we need to do all of the above.
class ModifiedGraphQLView(GraphQLView):
    # def __init__(self, **kwargs):
    #     kwargs.update({'batch':True})
    #     super(ModifiedGraphQLView, self).__init__(**kwargs)
    # graphiql_template = 'graphiql.html'

    def get_response(self, request, data, show_graphiql=False):

        query, variables, operation_name, id = self.get_graphql_params(request, data)

        execution_result = self.execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )

        status_code = 200
        if execution_result:
            response = {}

            if execution_result.errors:
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]

            if execution_result.invalid:
                status_code = 400
            else:
                response["data"] = execution_result.data

            if self.batch:
                response["id"] = id
                response["status"] = status_code

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None

        return result, status_code


    @staticmethod
    def get_graphql_params(request, data):
        request_type = request.META.get("CONTENT_TYPE", '')

        if "multipart/form-data" in request_type:
            query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, data)
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


    # def parse_body(self, request):
    #     content_type = self.get_content_type(request)
    #
    #     if content_type == "application/graphql":
    #         return {"query": request.body.decode()}
    #
    #     elif content_type == "application/json":
    #         # noinspection PyBroadException
    #         try:
    #             body = request.body.decode("utf-8")
    #         except Exception as e:
    #             raise HttpError(HttpResponseBadRequest(str(e)))
    #
    #         try:
    #             request_json = json.loads(body)
    #             if self.batch:
    #                 assert isinstance(request_json, list), (
    #                     "Batch requests should receive a list, but received {}."
    #                 ).format(repr(request_json))
    #                 assert (
    #                     len(request_json) > 0
    #                 ), "Received an empty list in the batch request."
    #             else:
    #                 assert isinstance(
    #                     request_json, dict
    #                 ), "The received data is not a valid JSON query."
    #             return request_json
    #         except AssertionError as e:
    #             raise HttpError(HttpResponseBadRequest(str(e)))
    #         except (TypeError, ValueError):
    #             raise HttpError(HttpResponseBadRequest("POST body sent invalid JSON."))
    #
    #     elif content_type in [
    #         "application/x-www-form-urlencoded",
    #         "multipart/form-data",
    #     ]:
    #         # operations = request.POST.get('operations')
    #         # map = request.POST.get('map')
    #         # json_operations = json.loads(operations)
    #         # json_map = json.loads(map)
    #         # result = {'map': json_map, 'operations': json_operations}
    #         # # import pdb; pdb.set_trace()
    #         # return result
    #         return request.POST
    #
    #
    #     return {}

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



class NewestGraphQLView(GraphQLView):
    def __init__(self, **kwargs):
        # kwargs.update({'batch':True})
        super(NewestGraphQLView, self).__init__(**kwargs)





    # def parse_body(self, request):
    #     content_type = self.get_content_type(request)
    #
    #     if content_type == "application/graphql":
    #         return {"query": request.body.decode()}
    #
    #     elif content_type == "application/json":
    #         # noinspection PyBroadException
    #         try:
    #             body = request.body.decode("utf-8")
    #             print('body', body)
    #         except Exception as e:
    #             raise HttpError(HttpResponseBadRequest(str(e)))
    #
    #         try:
    #             request_json = json.loads(body)
    #             if self.batch:
    #                 assert isinstance(request_json, list), (
    #                     "Batch requests should receive a list, but received {}."
    #                 ).format(repr(request_json))
    #                 assert (
    #                     len(request_json) > 0
    #                 ), "Received an empty list in the batch request."
    #             else:
    #                 assert isinstance(
    #                     request_json, dict
    #                 ), "The received data is not a valid JSON query."
    #             return request_json
    #         except AssertionError as e:
    #             raise HttpError(HttpResponseBadRequest(str(e)))
    #         except (TypeError, ValueError):
    #             raise HttpError(HttpResponseBadRequest("POST body sent invalid JSON."))
    #
    #     elif content_type in [
    #         "application/x-www-form-urlencoded",
    #         "multipart/form-data",
    #     ]:
    #         # import pdb; pdb.set_trace()
    #         body = request.POST.get('operations')
    #         request_json = json.loads(body)
    #         print('request_json', request_json)
    #         return request_json
    #
    #     return {}

    # class ObjectPath:

    # @staticmethod
    # def get_graphql_params(request, data):
    #     print('data', data)
    #     request_type = request.META.get("CONTENT_TYPE", '')
    #
    #     if "multipart/form-data" in request_type:
    #         import pdb; pdb.set_trace()
    #
    #         query, variables, operation_name, id = super(NewestGraphQLView, NewestGraphQLView).get_graphql_params(request, data)
    #
    #
    #     else:
    #         query, variables, operation_name, id = super(NewestGraphQLView, NewestGraphQLView).get_graphql_params(request, data)
    #
    #     return query, variables, operation_name, id
    #
    #
    #
    #
    #
    # def parse_body(self, request):
    #     content_type = self.get_content_type(request)
    #
    #     if content_type == "application/graphql":
    #         return {"query": request.body.decode()}
    #
    #     elif content_type == "application/json":
    #         # noinspection PyBroadException
    #         try:
    #             body = request.body.decode("utf-8")
    #         except Exception as e:
    #             raise HttpError(HttpResponseBadRequest(str(e)))
    #
    #         try:
    #             request_json = json.loads(body)
    #             if self.batch:
    #                 assert isinstance(request_json, list), (
    #                     "Batch requests should receive a list, but received {}."
    #                 ).format(repr(request_json))
    #                 assert (
    #                     len(request_json) > 0
    #                 ), "Received an empty list in the batch request."
    #             else:
    #                 assert isinstance(
    #                     request_json, dict
    #                 ), "The received data is not a valid JSON query."
    #             print('return val', request_json)
    #             return request_json
    #         except AssertionError as e:
    #             raise HttpError(HttpResponseBadRequest(str(e)))
    #         except (TypeError, ValueError):
    #             raise HttpError(HttpResponseBadRequest("POST body sent invalid JSON."))
    #
    #     elif content_type in [
    #         "application/x-www-form-urlencoded",
    #         "multipart/form-data",
    #     ]:
    #         # return request.POST
    #         # import pdb; pdb.set_trace()
    #
    #         body = request.POST.get('operations')
    #         request_json = json.loads(body)
    #
    #         if self.batch:
    #             return [request_json]
    #         else:
    #             return request_json
    #
    #
    #     return {}
