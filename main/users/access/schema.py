from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from main.users.models import User
from main.users.schema import UserType, UserPayload
from main.common import FieldError
from main.helpers import get_object, update_or_create, get_errors
import graphene
import graphql_jwt


class Tokens(graphene.ObjectType):
    # accessToken = graphql_jwt.ObtainJSONWebToken.Field()
    # refreshToken = graphql_jwt.Refresh.Field()
    accessToken = graphene.String()
    refreshToken = graphene.String()

    def resolve_accessToken(self, info, **kwargs):
        # ObtainJSONWebToken
        return ""

    def resolve_refreshToken(self, info, **kwargs):
        return "asdfasdf"


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    tokens = graphene.List(Tokens) # might be a list
    errors = graphene.List(FieldError) # errors: [FieldError!]

    def resolve_user(self, info, **kwargs):
        # get_object(User, kwargs['id'])
        # self.user contains the user info; not kwargs
        return User.objects.first()

    def resolve_tokens(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        # graphql_jwt.utils.

        return [Tokens]

    def resolve_errors(self, info, **kwargs):
        return [FieldError]


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


class Login(graphene.Mutation):
    class Arguments:
        #   login(input: LoginUserInput!): AuthPayload!
        input = graphene.Argument(LoginUserInput, required=True)
        # input = LoginUserInput(required=True)

    Output = AuthPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return AuthPayload(user=User(**input['input']))


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
        return None

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
