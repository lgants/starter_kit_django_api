from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from .models import (UserProfile, AuthCertificate, AuthFacebook, AuthGithub, AuthGoogle, AuthLinkedin)
from main.helpers import get_object, update_or_create, get_field_errors, get_errors
from main.common import FieldError
from django.contrib.auth import get_user_model
import graphene
from main.mixins import AuthType, AuthMutation
from main.permissions import AllowStaff, AllowAuthenticated
from django.core.exceptions import ValidationError



User = get_user_model()


class UserProfileType(AuthType, DjangoObjectType):
    # permission_classes = (AllowStaff,) # NOTE: works but implement permissions later

    firstName = graphene.String()
    lastName = graphene.String()
    fullName = graphene.String()

    class Meta:
        name = 'UserProfile'
        model = UserProfile


class AuthCertificateType(DjangoObjectType):
    class Meta:
        name = 'CertificateAuth'
        model = AuthCertificate

class AuthFacebookType(DjangoObjectType):
    class Meta:
        name = 'FacebookAuth'
        model = AuthFacebook

class AuthGithubType(DjangoObjectType):
    class Meta:
        name = 'GithubAuth'
        model = AuthGithub

class AuthGoogleType(DjangoObjectType):
    class Meta:
        name = 'GoogleAuth'
        model = AuthGoogle

class AuthLinkedinType(DjangoObjectType):
    class Meta:
        name = 'LinkedInAuth'
        model = AuthLinkedin


class UserAuthType(graphene.ObjectType):
    certificate = graphene.Field(AuthCertificateType)
    facebook = graphene.Field(AuthFacebookType)
    github = graphene.Field(AuthGithubType)
    google = graphene.Field(AuthGoogleType)
    linkedin = graphene.Field(AuthLinkedinType)

    class Meta:
        name = 'UserAuth'


class UserType(DjangoObjectType):
    # DjangoObjectType automatically includes fields on the model
    profile = graphene.Field(UserProfileType)
    auth = graphene.Field(UserAuthType)

    class Meta:
        name = 'User'
        model = User
        # only_fields=('id', 'username')
        exclude_fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser', 'role', 'date_joined', 'created_at', 'updated_at')


class UserPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    errors = graphene.List(FieldError) # [FieldError!] ???

    def resolve_user(self, info, **kwargs):
        return self.user

    def resolve_errors(self, info, **kwargs):
        return self.errors



class OrderByUserInput(graphene.InputObjectType):
  # # id | username | role | isActive | email
  column = graphene.String() # column: String
  # # asc | desc
  order = graphene.String() # order: String


class FilterUserInput(graphene.InputObjectType):
    # # search by username or email
    searchText = graphene.String() # searchText: String
    # # filter by role
    role = graphene.String() # role: String
    # # filter by isActive
    isActive = graphene.Boolean() # isActive: Boolean


class AuthCertificateInput(graphene.InputObjectType):
    serial = graphene.String() # serial: String


class AuthFacebookInput(graphene.InputObjectType):
    fbId = graphene.String() # fbId: String
    displayName = graphene.String() # displayName: String


class AuthGoogleInput(graphene.InputObjectType):
    googleId = graphene.String() # googleId: String
    displayName = graphene.String() # displayName: String


class AuthGitHubInput(graphene.InputObjectType):
    ghId = graphene.String() # ghId: String
    displayName = graphene.String() # displayName: String


class AuthLinkedInInput(graphene.InputObjectType):
    lnId = graphene.String() # lnId: String
    displayName = graphene.String() # displayName: String


class AuthInput(graphene.InputObjectType):
    certificate = AuthCertificateInput #certificate: AuthCertificateInput
    facebook = AuthFacebookInput #facebook: AuthFacebookInput
    google = AuthGoogleInput #google: AuthGoogleInput
    github = AuthGitHubInput #github: AuthGitHubInput
    linkedin = AuthLinkedInInput #linkedin: AuthLinkedInInput


class ProfileInput(graphene.InputObjectType):
    firstName = graphene.String()
    lastName = graphene.String()


# NOTE: this is used when signing up without external service
class AddUserInput(graphene.InputObjectType):
    username = graphene.String(required=True) # username: String!
    email = graphene.String(required=True) # email: String!
    password = graphene.String(required=True) # password: String!
    role = graphene.String(required=True) # role: String!
    isActive = graphene.Boolean() # isActive: Boolean
    profile = ProfileInput # profile: ProfileInput
    auth = AuthInput # auth: AuthInput

class EditUserInput(graphene.InputObjectType):
    id = graphene.Int(required=True) #id: Int!
    username = graphene.String() #username: String!
    role = graphene.String() #role: String!
    isActive = graphene.Boolean() #isActive: Boolean
    email = graphene.String()  #email: String!
    password = graphene.String() #NOTE: verify this works
    profile = ProfileInput
    auth = AuthInput


class UpdateUserPayload(graphene.ObjectType):
    mutation = graphene.String(required=True) #mutation: String!
    node = User #node: User!


class Query(graphene.ObjectType):
    user = graphene.Field(UserPayload, id=graphene.Int())
    users = graphene.List(UserType)

    current_user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        return get_object(User, kwargs['id'])

    def resolve_users(self, info, **kwargs):
        return User.objects.all() # TODO: modify to use pagination

    def resolve_current_user(self, info, **kwargs):
        if info.context.user.is_anonymous:
            return None
        else:
            return info.context.user


class AddUser(graphene.Mutation):
    class Arguments:
        # addUser(input: AddUserInput!): UserPayload!
        input = graphene.Argument(AddUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return None


class EditUser(AuthMutation, graphene.Mutation):
    permission_classes = (AllowAuthenticated,)

    class Arguments:
        # editUser(input: EditUserInput!): UserPayload!
        input = graphene.Argument(EditUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        try:
            edit_user_input = input.get('input', {})
            instance = get_object(User, edit_user_input.get('id'))

            if instance:
                user = update_or_create(instance, edit_user_input)
                return UserPayload(user=user)
        except ValidationError as e:
            return UserPayload(errors=get_field_errors(e))



        #
        # if cls.has_permission(context, info, input):
        #     instance = User()
        #     user = update_or_create(instance, input.get('input'))
        #
        #     return cls(**user)





class DeleteUser(graphene.Mutation):
    class Arguments:
        # deleteUser(id: Int!): UserPayload!
        id = graphene.Int(required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return None


class Mutation(graphene.ObjectType):
    # Create new user
    addUser = AddUser.Field()
    # Edit a user
    editUser = EditUser.Field()
    # Delete a user
    deleteUser = DeleteUser.Field()
