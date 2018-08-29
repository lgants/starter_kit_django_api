from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

# from .exceptions import GraphQLJWTError
# from .utils import get_authorization_header
from .utils import authenticate


class JSONWebTokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not hasattr(request, 'user') or request.user.is_anonymous:
            user = None
            try:
                user = authenticate(request)
            except:
                pass
            # except GraphQLJWTError as err:
            #     return JsonResponse({
            #         'errors': [{'message': str(err)}],
            #     }, status=401)

            if user is not None:
                request.user = request._cached_user = user
        # 'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM0NTcyNTM3LCJqdGkiOiJhZGE4YThhZWI0MDU0MmZkYjA5ZjJiNDAzMjRiMmMyNCIsInVzZXJfaWQiOjF9.tf8QnYjAbtCae_pDnyeB_TMmQo8Xoc_gHT0CSnE2osQ'
    #     if get_authorization_header(request) is not None:
    #         import pdb; pdb.set_trace()
    #         if not hasattr(request, 'user') or request.user.is_anonymous:
    #
    #             header = request.META.get('HTTP_AUTHORIZATION')
    #             token = header.split()[1]
    #             token_backend.decode(token)
    #
    #
    #
    #
    #             user = authenticate(request=request)
    #             # try:
    #             #     user = authenticate(request=request)
    #             # except GraphQLJWTError as err:
    #             #     return JsonResponse({
    #             #         'errors': [{'message': str(err)}],
    #             #     }, status=401)
    #
    #             if user is not None:
    #                 request.user = request._cached_user = user
    #
    # def process_response(self, request, response):
    #     patch_vary_headers(response, ('Authorization',))
    #     return response


class DisableCSRF(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            # Code to be executed for each request before
            # the view (and later middleware) are called.

            # NOTE: this is bad/unsecure; change to apply only if DEBUG=True and avoid csrf in deploy architecture with reverse proxies
            setattr(request, '_dont_enforce_csrf_checks', True)

            response = self.get_response(request)

            # Code to be executed for each request/response after
            # the view is called.

            return response
