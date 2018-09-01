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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from django.conf import settings
from rest_social_auth.views import BaseSocialAuthView, decorate_request
from social_django.utils import load_backend, load_strategy
from .decorators import social_auth
from .mixins import SocialAuthMixin
from .types import SocialType
import graphene
import graphql_jwt
import graphql_social_auth

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
        # TODO: add hook on User model to send email on User creation
        return self.user

    def resolve_tokens(self, info, **kwargs):
        refresh = RefreshToken.for_user(self.user)

        access_token = token_backend.encode(refresh.access.payload)
        refresh_token = token_backend.encode(refresh.payload)

        return Tokens(
            accessToken=access_token,
            refreshToken=refresh_token
        )

    def resolve_errors(self, info, **kwargs):
        # check if user is valid else return errors
        # return [FieldError]
        return None


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
    # username = graphene.String(required=True)
    # NOTE: only username currently works
    usernameOrEmail = graphene.String(required=True)
    password = graphene.String(required=True)


class AuthenticateInput(graphene.InputObjectType):
    provider = graphene.String(required=True)
    code = graphene.String(required=True)


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


class RefreshTokens(graphene.Mutation):
    class Arguments:
        # refreshTokens(refreshToken: String!): Tokens!
        refreshToken = graphene.String(required=True)

    Output = Tokens

    @classmethod
    def mutate(cls, context, info, **input):
        refresh = RefreshToken(input['refreshToken'])

        if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS'):
            if settings.SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION'):
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

        access_token = token_backend.encode(refresh.access_token.payload)
        refresh_token = token_backend.encode(refresh.payload)

        return Tokens(
            accessToken=access_token,
            refreshToken=refresh_token
        )


class Logout(graphene.Mutation):
    class Arguments:
        pass

    logout = graphene.String()

    @classmethod
    def mutate(cls, context, info, **input):
        logout(info.context)
        return cls(logout="ok")


class Login(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(LoginUserInput, required=True)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        username_field = User.USERNAME_FIELD

        # NOTE: need to change; currently uses username and NOT email
        user = authenticate(**{
            username_field: input['input']['usernameOrEmail'],
            'password': input['input']['password'],
        })

        if user is None or not user.is_active:
            # raise serializers.ValidationError(
            #     _('No active account found with given credentials'),
            # )
            pass
        else:
            login(info.context, user)

        return AuthPayload(user=user)


class Authenticate(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(AuthenticateInput)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        request = info.context
        input_data = input['input']

        provider = input_data['provider']
        code = input_data['code']

        request.auth_data = input_data
        decorate_request(request, provider)

        user = User()
        manual_redirect_uri = request.auth_data.pop('redirect_uri', None)

        request.backend.redirect_uri = settings.REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI

        request.backend.REDIRECT_STATE = False
        request.backend.STATE_PARAMETER = False

        user = request.backend.auth_complete()

        if user is None or not user.is_active:
            # raise serializers.ValidationError(
            #     _('No active account found with given credentials'),
            # )
            pass
        else:
            login(info.context, user)

        return AuthPayload(user=user)


class Mutation(graphene.ObjectType):
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
    logout = Logout.Field()
    # Authenticate user
    authenticate = Authenticate.Field()
