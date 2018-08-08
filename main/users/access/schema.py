from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from main.users.models import User
from main.users.schema import UserType, UserPayload
from main.helpers import get_object, update_or_create, get_errors
import graphene


class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()

    def resole_field(self, info, **kwargs):
        return "error"

    def resole_message(self, info, **kwargs):
        return "message"


class Tokens(graphene.ObjectType):
    accessToken = graphene.String()
    refreshToken = graphene.String()

    def resolve_accessToken(self, info, **kwargs):
        return "asdfadsfasdf"

    def resolve_refreshToken(self, info, **kwargs):
        return "asdfasdf"


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    tokens = graphene.List(Tokens) # might be a list
    errors = graphene.List(FieldError) # errors: [FieldError!]

    def resolve_user(self, info, **kwargs):
        return User.objects.first()

    def resolve_tokens(self, info, **kwargs):
        return ["asdf"]


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


class Login(graphene.Mutation):
    class Arguments:
        #   login(input: LoginUserInput!): AuthPayload!
        input = graphene.Argument(LoginUserInput)
        # input = LoginUserInput(required=True)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return AuthPayload


class ForgotPassword(graphene.Mutation):
    class Arguments:
        #   forgotPassword(input: ForgotPasswordInput!): String
        input = graphene.Argument(ForgotPasswordInput)

    message = graphene.String()

    @classmethod
    def mutate(cls, context, info, **input):
        return cls(message="")


class ResetPassword(graphene.Mutation):
    class Arguments:
        #   resetPassword(input: ResetPasswordInput!): ResetPayload!
        input = graphene.Argument(ResetPasswordInput)

    Output = ResetPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return ResetPayload


class Register(graphene.Mutation):
    class Arguments:
        # register(input: RegisterUserInput!): UserPayload!
        input = graphene.Argument(RegisterUserInput)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return UserPayload

class RefreshTokens(graphene.Mutation):
    class Arguments:
        # refreshTokens(refreshToken: String!): Tokens!
        refresh_token = graphene.String(required=True)

    Output = Tokens

    @classmethod
    def mutate(cls, context, info, **input):
        return Tokens

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
