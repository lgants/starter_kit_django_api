from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from main.users.models import User
from main.users.schema import UserType
from main.helpers import get_object, update_or_create, get_errors
import graphene



class Tokens(graphene.ObjectType):
    accessToken = graphene.String()
    refreshToken = graphene.String()

    def resolve_accessToken(self, info, **kwargs):
        return None

    def resolve_refreshToken(self, info, **kwargs):
        return None


class AuthPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    tokens = graphene.List(Tokens) # might be a list
    # errors: [FieldError!] # ???

    def resolve_user(self, info, **kwargs):
        return User.objects.first()

    def resolve_tokens(self, info, **kwargs):
        return ["asdf"]
        
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



class LoginUserInput(graphene.InputObjectType):
    usernameOrEmail = graphene.String(required=True)
    password = graphene.String(required=True)

# class CreatePerson(graphene.Mutation):
#     class Arguments:
#         person_data = PersonInput(required=True)
#
#     person = graphene.Field(Person)




class Login(graphene.Mutation):
    class Arguments:
        # person_data = PersonInput(required=True)
        input = LoginUserInput(required=True)
        # password = graphene.String
        #   login(input: LoginUserInput!): AuthPayload!
        # input = graphene.Argument(LoginUserInput)
        # input = LoginUserInput(required=True)

    AuthPayload = graphene.Field(AuthPayload)

    @staticmethod
    def mutate(root, info, **kwargs):
        return None

    # @classmethod
    # def mutate(cls, context, info, **input):
    #     # return AuthPayload
    #     return cls(user=User.objects.first())

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
