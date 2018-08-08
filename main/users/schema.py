from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from .models import (User, UserProfile, AuthCertificate, AuthFacebook, AuthGithub, AuthGoogle, AuthLinkedin)
from main.helpers import get_object
from main.common import FieldError
import graphene


class UserProfileType(DjangoObjectType):
    firstName = graphene.String()
    lastName = graphene.String()
    fullName = graphene.String()

    class Meta:
        name = "UserProfile"
        model = UserProfile


class AuthCertificateType(DjangoObjectType):
    class Meta:
        name = "CertificateAuth"
        model = AuthCertificate

class AuthFacebookType(DjangoObjectType):
    class Meta:
        name = "FacebookAuth"
        model = AuthFacebook

class AuthGithubType(DjangoObjectType):
    class Meta:
        name = "GithubAuth"
        model = AuthGithub

class AuthGoogleType(DjangoObjectType):
    class Meta:
        name = "GoogleAuth"
        model = AuthGoogle

class AuthLinkedinType(DjangoObjectType):
    class Meta:
        name = "LinkedInAuth"
        model = AuthLinkedin


class UserAuthType(graphene.ObjectType):
    certificate = graphene.Field(AuthCertificateType)
    facebook = graphene.Field(AuthFacebookType)
    github = graphene.Field(AuthGithubType)
    google = graphene.Field(AuthGoogleType)
    linkedin = graphene.Field(AuthLinkedinType)

    class Meta:
        name = "UserAuth"


class UserType(DjangoObjectType):
    profile = graphene.Field(UserProfileType)
    auth = graphene.Field(UserAuthType)

    class Meta:
        name = "User"
        model = User



class UserPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    errors = graphene.List(FieldError) # [FieldError!] ???

    def resolve_user(self, info, **kwargs):
        return User.objects.first()

    def resolve_errors(self, info, **kwargs):
        return []



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


class AddUserInput(graphene.InputObjectType):
    username = graphene.String(required=True) # username: String!
    email = graphene.String(required=True) # email: String!
    password = graphene.String(required=True) # password: String!
    role = graphene.String(required=True) # role: String!
    isActive = graphene.Boolean() # isActive: Boolean
    profile = ProfileInput # profile: ProfileInput
    auth = AuthInput # auth: AuthInput

class EditUserInput(graphene.InputObjectType):
    id = graphene.Int() #id: Int!
    username = graphene.String() #username: String!
    role = graphene.String() #role: String!
    isActive = graphene.Boolean() #isActive: Boolean
    email = graphene.String()  #email: String!
    password = graphene.String()
    profile = ProfileInput
    auth = AuthInput


class UpdateUserPayload(graphene.ObjectType):
    mutation = graphene.String(required=True) #mutation: String!
    node = User #node: User!


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    current_user = graphene.Field(UserType, id=graphene.Int())

    def resolve_current_user(self, info, **kwargs):
        return None
        # return get_object(User, kwargs['id'])

    def resolve_user(self, info, **kwargs):
        return get_object(User, kwargs['id'])

    def resolve_users(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        return User.objects.all()
