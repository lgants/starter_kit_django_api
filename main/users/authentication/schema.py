from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from main.users.models import User
import graphene


class LoginUserInput(graphene.ObjectType):
    usernameOrEmail = graphene.String()
    password = graphene.String()


class Tokens(graphene.ObjectType):
    accessToken = graphene.String()
    refreshToken = graphene.String()


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(User)
    tokens = graphene.Field(Tokens) # might be a list
    # errors: [FieldError!] # ???


class RegisterUserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class ForgotPasswordInput(graphene.InputObjectType):
    email = graphene.String()


class ResetPasswordInput(graphene.InputObjectType):
    token = graphene.String()
    password = graphene.String()
    passwordConfirmation = graphene.String()


class ResetPayload(graphene.ObjectType):
    # errors: [FieldError!] # ???
    pass



# extend type Mutation {
#   # Login user
#   login(input: LoginUserInput!): AuthPayload!
#   # Forgot password
#   forgotPassword(input: ForgotPasswordInput!): String
#   # Reset password
#   resetPassword(input: ResetPasswordInput!): ResetPayload!
#   # Register user
#   register(input: RegisterUserInput!): UserPayload!
# }
