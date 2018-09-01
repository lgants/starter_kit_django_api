# NOTE: this works, but don't plan to no longer plan to support oauth tokens
# from django.contrib.auth import authenticate
# from django.http import JsonResponse
# from django.utils.cache import patch_vary_headers
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.settings import api_settings
# from django.contrib.auth import get_user_model
#
# # from .exceptions import GraphQLJWTError
# # from .utils import get_authorization_header
#
# User = get_user_model()
#
#
# class JSONWebTokenMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         if not hasattr(request, 'user') or request.user.is_anonymous:
#             user = None
#             try:
#                 user = authenticate(request)
#             except:
#                 pass
#             # except GraphQLJWTError as err:
#             #     return JsonResponse({
#             #         'errors': [{'message': str(err)}],
#             #     }, status=401)
#
#             if user is not None:
#                 request.user = request._cached_user = user
#         # 'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM0NTcyNTM3LCJqdGkiOiJhZGE4YThhZWI0MDU0MmZkYjA5ZjJiNDAzMjRiMmMyNCIsInVzZXJfaWQiOjF9.tf8QnYjAbtCae_pDnyeB_TMmQo8Xoc_gHT0CSnE2osQ'
#     #     if get_authorization_header(request) is not None:
#     #         import pdb; pdb.set_trace()
#     #         if not hasattr(request, 'user') or request.user.is_anonymous:
#     #
#     #             header = request.META.get('HTTP_AUTHORIZATION')
#     #             token = header.split()[1]
#     #             token_backend.decode(token)
#     #
#     #
#     #
#     #
#     #             user = authenticate(request=request)
#     #             # try:
#     #             #     user = authenticate(request=request)
#     #             # except GraphQLJWTError as err:
#     #             #     return JsonResponse({
#     #             #         'errors': [{'message': str(err)}],
#     #             #     }, status=401)
#     #
#     #             if user is not None:
#     #                 request.user = request._cached_user = user
#     #
#     # def process_response(self, request, response):
#     #     patch_vary_headers(response, ('Authorization',))
#     #     return response
#
# def authenticate(request):
#     header = get_header(request)
#     if header is None:
#         return None
#
#     raw_token = get_raw_token(header)
#     if raw_token is None:
#         return None
#
#     validated_token = get_validated_token(raw_token)
#
#     # return get_user(validated_token), None
#     return get_user(validated_token)
#
# # def authenticate_header(self, request):
# #     return '{0} realm="{1}"'.format(
# #         api_settings.AUTH_HEADER_TYPE,
# #         self.www_authenticate_realm,
# #     )
#
# def get_authorization_header(request):
#     # import pdb; pdb.set_trace()
#     auth = request.META.get('HTTP_AUTHORIZATION', '').split()
#     # auth = request.META.get(jwt_settings.JWT_AUTH_HEADER, '').split()
#     # prefix = jwt_settings.JWT_AUTH_HEADER_PREFIX
#
#     # if len(auth) != 2 or auth[0].lower() != prefix.lower():
#     if len(auth) != 2:
#         return None
#     return auth[1]
#
#
# def get_header(request):
#     """
#     Extracts the header containing the JSON web token from the given
#     request.
#     """
#     header = request.META.get('HTTP_AUTHORIZATION')
#
#     # if isinstance(header, text_type):
#     #     # Work around django test client oddness
#     #     header = header.encode(HTTP_HEADER_ENCODING)
#
#     return header
#
#
# def get_raw_token(header):
#     """
#     Extracts an unvalidated JSON web token from the given header.
#     """
#     parts = header.split()
#
#     # if parts[0] != AUTH_HEADER_TYPE_BYTES:
#     #     # Assume the header does not contain a JSON web token
#     #     return None
#
#     if len(parts) != 2:
#         # raise AuthenticationFailed(
#         #     _('Authorization header must contain two space-delimited values'),
#         #     code='bad_authorization_header',
#         # )
#         pass
#
#     return parts[1]
#
#
# def get_validated_token(raw_token):
#     """
#     Validates an encoded JSON web token and returns a validated token
#     wrapper object.
#     """
#     messages = []
#     for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
#         try:
#             return AuthToken(raw_token)
#         except TokenError as e:
#             # messages.append({'token_class': AuthToken.__name__,
#             #                  'token_type': AuthToken.token_type,
#             #                  'message': e.args[0]})
#             pass
#
#     # raise InvalidToken({
#     #     'detail': _('Given token not valid for any token type'),
#     #     'messages': messages,
#     # })
#
#
# def get_user(validated_token):
#     """
#     Attempts to find and return a user using the given validated token.
#     """
#     try:
#         user_id = validated_token[api_settings.USER_ID_CLAIM]
#     except KeyError:
#         # raise InvalidToken(_('Token contained no recognizable user identification'))
#         pass
#
#     try:
#         user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
#     except User.DoesNotExist:
#         # raise AuthenticationFailed(_('User not found'), code='user_not_found')
#         pass
#
#     if not user.is_active:
#         # raise AuthenticationFailed(_('User is inactive'), code='user_inactive')
#         pass
#
#     return user






# NOTE: works but don't want to use
# class DisableCSRF(object):
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#             # Code to be executed for each request before
#             # the view (and later middleware) are called.
#
#             # NOTE: this is bad/unsecure; change to apply only if DEBUG=True and avoid csrf in deploy architecture with reverse proxies
#             setattr(request, '_dont_enforce_csrf_checks', True)
#
#             response = self.get_response(request)
#
#             # Code to be executed for each request/response after
#             # the view is called.
#
#             return response
