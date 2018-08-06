from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from main.users.models import User
from main.helpers import get_object, update_or_create, get_errors
import graphene



class Tokens(graphene.ObjectType):
    accessToken = graphene.String()
    refreshToken = graphene.String()


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(User)
    tokens = graphene.Field(Tokens) # might be a list
    # errors: [FieldError!] # ???


class LoginUserInput(graphene.InputObjectType):
    usernameOrEmail = graphene.String(required=True)
    password = graphene.String(required=True)

#
# class ForgotPasswordInput(graphene.InputObjectType):
#     email = graphene.String()
#
#
# class ResetPasswordInput(graphene.InputObjectType):
#     token = graphene.String()
#     password = graphene.String()
#     passwordConfirmation = graphene.String()
#
#
# class RegisterUserInput(graphene.InputObjectType):
#     username = graphene.String()
#     email = graphene.String()
#     password = graphene.String()
#
#
# class ResetPayload(graphene.ObjectType):
#     # errors: [FieldError!] # ???
#     pass

class Login(graphene.Mutation):
    class Arguments:
        #   login(input: LoginUserInput!): AuthPayload!
        # input = graphene.Argument(LoginUserInput(required=True))
        input = LoginUserInput(required=True)

    # AuthPayload = graphene.Field(AuthPayload)

    @classmethod
    def mutate(cls, context, info, **input):
        return None

# class ForgotPassword(graphene.Mutation):
#     class Arguments:
#         #   forgotPassword(input: ForgotPasswordInput!): String
#         input = graphene.Argument(ForgotPasswordInput)
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         return None
#
#
# class ResetPassword(graphene.Mutation):
#     class Arguments:
#         #   resetPassword(input: ResetPasswordInput!): ResetPayload!
#         input = graphene.Argument(ForgotPasswordInput)
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         return None
#
#
# class Register(graphene.Mutation):
#     class Arguments:
#         # register(input: RegisterUserInput!): UserPayload!
#         input = graphene.Argument(ForgotPasswordInput)
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         return None


class Mutation(graphene.ObjectType):
    # # Login user
    login = Login.Field()
    # # Forgot password
    # forgotPassword = ForgotPassword.Field()
    # # Reset password
    # resetPassword = ResetPassword.Field()
    # # Register user
    # register = Register.Field()
    pass
