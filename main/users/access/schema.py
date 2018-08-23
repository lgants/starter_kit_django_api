from django.contrib.auth import authenticate
from django.utils.six import text_type
from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from graphene_django.rest_framework.mutation import SerializerMutation
# from main.users.models import User
from django.contrib.auth import get_user_model, login, logout
from main.users.schema import UserType, UserPayload
from main.common import FieldError
from main.helpers import get_object, update_or_create, get_errors
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)
from rest_framework_simplejwt.tokens import (
    RefreshToken
)
from rest_framework_simplejwt.state import (
    token_backend
)
from rest_framework_simplejwt.backends import (
    TokenBackend
)
# from rest_social_auth.views import (
#     decorate_request,
#     set_input_data,
#     get_serializer_in,
#     get_serializer_in_data
# )
from django.conf import settings
from rest_social_auth.views import BaseSocialAuthView, decorate_request
from social_django.utils import load_backend, load_strategy
import graphene
import graphql_jwt
import graphql_social_auth
from .decorators import social_auth
from .mixins import SocialAuthMixin
from .types import SocialType

User = get_user_model()


class Tokens(graphene.ObjectType):
    accessToken = graphene.String()
    refreshToken = graphene.String()

    def resolve_accessToken(self, info, **kwargs):
        return self.accessToken

    def resolve_refreshToken(self, info, **kwargs):
        return self.refreshToken


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    tokens = graphene.Field(Tokens) # might be a list
    errors = graphene.List(FieldError) # errors: [FieldError!]

    def resolve_user(self, info, **kwargs):

        # get_object(User, kwargs['id'])
        # self.user contains the user info; not kwargs
        # TODO: add hook on User model to send email on User creation
        return self.user

    def resolve_tokens(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        # graphql_jwt.utils.
        # TODO: CREATE TOKENS HERE AND PASS AS ARG

        # return [Tokens]
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token

        access_token = token_backend.encode(access.payload)
        refresh_token = token_backend.encode(refresh.payload)

        return Tokens(accessToken=access_token, refreshToken=refresh_token)

    def resolve_errors(self, info, **kwargs):
        # check if user is valid else return errors
        # return [FieldError]
        return None


# class AuthPayload(graphql_jwt.JSONWebTokenMutation):
#     user = graphene.Field(UserType)
#     # tokens = graphene.List(Tokens) # might be a list
#     # errors = graphene.List(FieldError) # errors: [FieldError!]
#
#     @classmethod
#     def resolve(cls, root, info):
#         return cls(user=info.context.user)
#
#     # def resolve_user(self, info, **kwargs):
#     #     get_object(User, kwargs['id'])
#
#     # def resolve_tokens(self, info, **kwargs):
#     #     return [Tokens]
#     #
#     # def resolve_errors(self, info, **kwargs):
#     #     return [FieldError]


class ResetPayload(graphene.ObjectType):
    errors = graphene.List(FieldError) # errors: [FieldError!]


class ForgotPasswordInput(graphene.InputObjectType):
    email = graphene.String()


class ResetPasswordInput(graphene.InputObjectType):
    token = graphene.String()
    password = graphene.String()
    passwordConfirmation = graphene.String()


class RegisterUserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class LoginUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    # usernameOrEmail = graphene.String(required=True)
    password = graphene.String(required=True)


class AuthenticateInput(graphene.InputObjectType):
    provider = graphene.String(required=True)
    code = graphene.String(required=True)


# class Login(graphene.Mutation):
#     class Arguments:
#         #   login(input: LoginUserInput!): AuthPayload!
#         input = graphene.Argument(LoginUserInput, required=True)
#         # input = LoginUserInput(required=True)
#
#     Output = AuthPayload
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         return AuthPayload(user=User(**input['input']))


class ForgotPassword(graphene.Mutation):
    class Arguments:
        #   forgotPassword(input: ForgotPasswordInput!): String
        input = graphene.Argument(ForgotPasswordInput, required=True)

    message = graphene.String()

    @classmethod
    def mutate(cls, context, info, **input):
        return cls(message="")


class ResetPassword(graphene.Mutation):
    class Arguments:
        #   resetPassword(input: ResetPasswordInput!): ResetPayload!
        input = graphene.Argument(ResetPasswordInput, required=True)

    Output = ResetPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return ResetPayload


class Register(graphene.Mutation):
    class Arguments:
        # register(input: RegisterUserInput!): UserPayload!
        input = graphene.Argument(RegisterUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return UserPayload(user=User(**input['input']))
        # return UserPayload(user)


class RefreshTokens(graphene.Mutation):
    class Arguments:
        # refreshTokens(refreshToken: String!): Tokens!
        refresh_token = graphene.String(required=True)

    Output = Tokens

    @classmethod
    def mutate(cls, context, info, **input):
        return Tokens


class Logout(graphene.Mutation):
    @classmethod
    def mutate(cls, context, info, **input):
        logout(info.context)
        return None


# class Token(SerializerMutation):
#     class Meta:
#         serializer_class = TokenObtainPairSerializer
#
#     Output = Tokens


# class TokenMixin(object):
#     @classmethod
#     def get_token(cls, user):
#         raise NotImplemented('Must implement `get_token` method for `TokenObtainSerializer` subclasses')
#
#     @classmethod
#     def validate(cls, attrs):
#         username_field = User.USERNAME_FIELD
#
#         print("attrs", attrs)
#         # import pdb; pdb.set_trace()
#
#         # NOTE: MUST use get_user_model when creating users AND MUST set is_active on user to True
#         user = authenticate(**{
#             username_field: attrs[username_field],
#             'password': attrs['password'],
#         })
#
#         if user is None or not user.is_active:
#             raise Exception('No active account found with the given credentials')
#
#         # return {}
#         return user


# class Token(TokenMixin, graphene.Mutation):
#     class Arguments:
#         input = graphene.Argument(LoginUserInput, required=True)
#
#     Output = Tokens
#
#     @classmethod
#     def get_token(cls, user):
#         return RefreshToken.for_user(user)
#
#     @classmethod
#     def aggregate(cls, attrs):
#         user = super(Token, cls).validate(attrs)
#
#         refresh = cls.get_token(user)
#
#         import pdb; pdb.set_trace()
#
#         data = {}
#         data['refresh'] = text_type(refresh)
#         data['access'] = text_type(refresh.access_token)
#
#         return data, user
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         attrs = input['input']
#         data, user = cls.aggregate(attrs)
#
#         import pdb; pdb.set_trace()
#
#         # TODO: self is undefined
#         token = cls.get_token(user)
#
#
#         return Tokens


class Login(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(LoginUserInput, required=True)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        username_field = User.USERNAME_FIELD

        ###### THIS WORKS ######
        # user = authenticate(**{
        #     username_field: input['input'][username_field],
        #     'password': input['input']['password'],
        # })
        #
        # if user is None or not user.is_active:
        #     # raise serializers.ValidationError(
        #     #     _('No active account found with given credentials'),
        #     # )
        #     pass
        # else:
        #     login(info.context, user)
        #
        # return AuthPayload(user=user)
        ###### THIS WORKS ######
        user = User.objects.all()[0]

        return AuthPayload(user=user)



class SocialAuth(SocialAuthMixin, graphene.Mutation):
    # NOTE: WIP
    # https://github.com/st4lk/django-rest-social-auth/blob/master/rest_social_auth/views.py
    social = graphene.Field(SocialType)

    # class Meta:
    #     abstract = True

    class Arguments:
        provider = graphene.String(required=True)
        access_token = graphene.String(required=True)

    @classmethod
    @social_auth
    def mutate(cls, root, info, social, **kwargs):
        return cls.resolve(root, info, social, **kwargs)


class Authenticate(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(AuthenticateInput)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        # TODO ADD LOGIC HERE
        provider = input['input']['provider']
        code = input['input']['code']

        # strategy = load_strategy(info.context)
        # backend = load_backend(strategy, provider, redirect_uri=None)
        # user = backend.do_auth(code)

        # BaseSocialAuthView
        # input_data = self.get_serializer_in_data()
        # set_input_data(request, input_data)
        # decorate_request(info.context, provider)

        input_data = input['input']
        request = info.context

        request.auth_data = input_data
        decorate_request(request, provider)

        # user = request.user or None
        user = User()
        manual_redirect_uri = request.auth_data.pop('redirect_uri', None)
        # manual_redirect_uri = get_redirect_uri(manual_redirect_uri)

        request.backend.redirect_uri = settings.REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI

        request.backend.REDIRECT_STATE = False
        request.backend.STATE_PARAMETER = False

        # return {
        #     'grant_type': 'authorization_code',
        #     'code': self.data['code']
        # }
        user = request.backend.auth_complete()

        # NOTE: user is saved at this point
        # meh = {'_state': <django.db.models.base.ModelState object at 0x1055ba3c8>, 'id': 3, 'password': '!ZyNmL2RBp2hBcuKl5NMsUkBF9A5xDmyZoQZ7mT6p', 'last_login': None, 'is_superuser': False, 'first_name': 'Logan', 'last_name': '', 'is_staff': False, 'date_joined': datetime.datetime(2018, 8, 22, 2, 15, 15, 563286, tzinfo=<UTC>), 'username': 'lgants', 'email': 'lgants@gmail.com', 'role': 'user', 'is_active': False, 'created_at': datetime.datetime(2018, 8, 22, 2, 15, 15, 563845, tzinfo=<UTC>), 'updated_at': datetime.datetime(2018, 8, 22, 2, 15, 15, 573143, tzinfo=<UTC>), 'social_user': <UserSocialAuth: lgants>, 'is_new': False, 'backend': 'social_core.backends.github.GithubOAuth2'}
        if user is None or not user.is_active:
            # raise serializers.ValidationError(
            #     _('No active account found with given credentials'),
            # )
            pass
        else:
            login(info.context, user)

        # {'input': {'provider': 'github', 'code': '123456'}}
        return AuthPayload(user=user)


class Mutation(graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    # Login user
    login = Login.Field()
    # Forgot password
    forgotPassword = ForgotPassword.Field()
    # Reset password
    resetPassword = ResetPassword.Field()
    # Register user
    register = Register.Field()
    # Refresh user tokens
    refreshTokens = RefreshTokens.Field()
    # Logout user
    logout = Login.Field()

    # token = Token.Field()

    socialAuth = SocialAuth.Field()

    authenticate = Authenticate.Field()
