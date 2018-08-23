from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from .models import (UserProfile, AuthCertificate, AuthFacebook, AuthGithub, AuthGoogle, AuthLinkedin)
from main.helpers import get_object
from main.common import FieldError
from django.contrib.auth import get_user_model
import graphene


User = get_user_model()


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
    # DjangoObjectType automatically includes fields on the model
    profile = graphene.Field(UserProfileType)
    auth = graphene.Field(UserAuthType)

    class Meta:
        name = "User"
        model = User


    # def resolve_profile(self, info, **kwargs):
    #     pass
    #
    # def resolve_auth(self, info, **kwargs):
    #     # self is user
    #     # TODO: generate the auth tokens here  ???
    #     # import pdb; pdb.set_trace()
    #     pass




class UserPayload(graphene.ObjectType):
    user = graphene.Field(UserType)
    errors = graphene.List(FieldError) # [FieldError!] ???

    def resolve_user(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        # fields = [f.name for f in User._meta.get_fields()]
        # obj = self.user.__dict__
        # _user = {k: obj[k] for k in set(fields) & set(obj.keys())}
        #
        # return User(**_user)
        return self

    def resolve_errors(self, info, **kwargs):
        # check if user is valid with self.user
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
    user = graphene.Field(UserPayload, id=graphene.Int())
    users = graphene.List(UserType)

    current_user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        # import pdb; pdb.set_trace()
        # return UserPayload
        # return User.objects.first()
        return get_object(User, kwargs['id'])

    def resolve_users(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        return User.objects.all()

    def resolve_current_user(self, info, **kwargs):
        # print(info.context.user)
        # return info.context.user

        return User.objects.all()[0]


        # import pdb; pdb.set_trace()
        # print(info.context.user)
        # return info.context.user
        # return User.objects.all()[0]
        # if info.context.user.is_anonymous:
        # # if not info.context.user.is_authenticated()
        #     # return User.objects.none()
        #     return None
        # else:
        #     return info.context.user


class AddUser(graphene.Mutation):
    class Arguments:
        # addUser(input: AddUserInput!): UserPayload!
        input = graphene.Argument(AddUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return None


class EditUser(graphene.Mutation):
    class Arguments:
        # editUser(input: EditUserInput!): UserPayload!
        input = graphene.Argument(EditUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        return None


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
