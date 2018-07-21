from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from .models import (User, UserProfile, AuthCertificate, AuthFacebook, AuthGithub, AuthGoogle, AuthLinkedin)
from main.users import User
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
    errors: [FieldError!] # ???


class RegisterUserInput(graphene.ObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class ForgotPasswordInput(graphene.ObjectType):
    email = graphene.String()


class ResetPasswordInput(graphene.ObjectType):
    token = graphene.String()
    password = graphene.String()
    passwordConfirmation = graphene.String()


class ResetPayload(graphene.ObjectType):
    errors: [FieldError!] # ???
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
