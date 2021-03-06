from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.conf import settings
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from rest_social_auth.views import decorate_request
# from graphene_django_subscriptions.subscription import Subscription
from graphene_django import DjangoObjectType
# from graphql.error import GraphQLError
from main.users.schema import UserType, UserPayload
from main.common import FieldError
from main.helpers import get_object, update_or_create, get_errors, get_field_errors
from main.permissions import AllowAny, AllowAuthenticated
from main.mixins import AuthType, AuthMutation
from social_django.utils import load_backend, load_strategy
from .decorators import social_auth
from .types import SocialType
import graphql_social_auth
import graphql_jwt
import graphene


User = get_user_model()


class Tokens(graphene.ObjectType):
    accessToken = graphene.String()
    refreshToken = graphene.String()

    def resolve_accessToken(self, info, **kwargs):
        return self.accessToken

    def resolve_refreshToken(self, info, **kwargs):
        return self.refreshToken


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(UserType) # user: User
    tokens = graphene.Field(Tokens) # tokens: Tokens
    errors = graphene.List(FieldError) # errors: [FieldError!]

    def resolve_user(self, info, **kwargs):
        # TODO: add hook on User model to send email on User creation
        return self.user

    def resolve_tokens(self, info, **kwargs):
        if self.user:
            refresh = RefreshToken.for_user(self.user)
            access = refresh.access_token

            access_token = token_backend.encode(access.payload)
            refresh_token = token_backend.encode(refresh.payload)

            return Tokens(
                accessToken=access_token,
                refreshToken=refresh_token
            )
        else:
            return None

    def resolve_errors(self, info, **kwargs):
        return self.errors


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


# TODO: implement
class ResetPassword(graphene.Mutation):
    class Arguments:
        #   resetPassword(input: ResetPasswordInput!): ResetPayload!
        input = graphene.Argument(ResetPasswordInput, required=True)

    Output = ResetPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return ResetPayload


class Register(AuthMutation, graphene.Mutation):
    permission_classes = (AllowAny,)

    class Arguments:
        # register(input: RegisterUserInput!): UserPayload!
        input = graphene.Argument(RegisterUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        if cls.has_permission(context, info, input):
            try:
                register_user_input = input.get('input', {})

                user = User.objects.create_user(**register_user_input)
                return UserPayload(user=user)
            except ValidationError as e:
                return UserPayload(errors=get_field_errors(e))


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
        login_user_input = input.get('input', {})
        usernameOrEmail = login_user_input.get('usernameOrEmail')
        password = login_user_input.get('password')

        try:
            user = User.objects.get_or_none(Q(username__iexact=usernameOrEmail) | Q(email__iexact=usernameOrEmail))

            if user is None:
                raise ValidationError({'usernameOrEmail': 'Please enter a valid Username or Email.'})

            # TODO: generic error not configured
            if not user.is_active:
                raise PermissionError('No active account found with given credentials')

            if user.check_password(password):
                login(info.context, user, backend='django.contrib.auth.backends.ModelBackend')
                return AuthPayload(user=user)
            else:
                raise ValidationError({'password': 'Invalid password'})

        except ValidationError as e:
            return AuthPayload(errors=get_field_errors(e))


class Authenticate(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(AuthenticateInput)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        try:
            authenticate_user_input = input.get('input', {})
            provider = authenticate_user_input.get('provider')
            code = authenticate_user_input.get('code')
            request = info.context

            request.auth_data = authenticate_user_input

            decorate_request(request, provider)

            manual_redirect_uri = request.auth_data.pop('redirect_uri', None)

            request.backend.redirect_uri = settings.REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI
            request.backend.REDIRECT_STATE = False
            request.backend.STATE_PARAMETER = False

            user = request.backend.auth_complete()

            # NOTE: will raise exception unless is_active == True; always false initially
            # if user is None or not user.is_active:
            #     raise ValidationError('No active account found with given credentials.')
            # else:
            #     login(request, user)
            if user is not None: login(request, user)

            return AuthPayload(user=user)
        except ValidationError as e:
            return AuthPayload(errors=get_field_errors(e))


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
