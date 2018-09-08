from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import get_user_model
from django.db import transaction
from graphene_django import DjangoObjectType
# from graphene_django_subscriptions.subscription import Subscription
from graphene_django_subscriptions.subscription import Subscription
from main.helpers import get_object, update_or_create, get_errors, get_field_errors
from main.permissions import AllowAny, AllowAuthenticated, AllowOwnerOrSuperuser
from main.mixins import AuthType, AuthMutation
from main.common import FieldError
from .models import (
    UserProfile,
    AuthCertificate,
    AuthFacebook,
    AuthGithub,
    AuthGoogle,
    AuthLinkedin
)
from .serializers import (
    UserSerializer
)
import graphene


User = get_user_model()


class UserProfileType(AuthType, DjangoObjectType):
    # permission_classes = (AllowAny,)

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
        # exclude_fields = ('fb_id', 'display_name')


class AuthGithubType(DjangoObjectType):
    class Meta:
        name = 'GithubAuth'
        model = AuthGithub
        # exclude_fields = ('gh_id', 'display_name')


class AuthGoogleType(DjangoObjectType):
    class Meta:
        name = 'GoogleAuth'
        model = AuthGoogle
        # exclude_fields = ('google_id', 'display_name')


class AuthLinkedinType(DjangoObjectType):
    class Meta:
        name = 'LinkedInAuth'
        model = AuthLinkedin
        # exclude_fields = ('ln_id', 'display_name')


class UserAuthType(graphene.ObjectType):
    certificate = graphene.Field(AuthCertificateType)
    facebook = graphene.Field(AuthFacebookType)
    github = graphene.Field(AuthGithubType)
    google = graphene.Field(AuthGoogleType)
    linkedin = graphene.Field(AuthLinkedinType)

    class Meta:
        name = 'UserAuth'


class UserType(DjangoObjectType):
    profile = graphene.Field(UserProfileType)
    auth = graphene.Field(UserAuthType)

    class Meta:
        name = 'User'
        model = User
        # NOTE: exclusion of these fields currently breaks everything
        # exclude_fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'created_at', 'updated_at')


class UserPayload(graphene.ObjectType):
    user = graphene.Field(UserType) # User
    errors = graphene.List(FieldError) # [FieldError!]

    def resolve_user(self, info, **kwargs):
        return self.user

    def resolve_errors(self, info, **kwargs):
        return self.errors


class OrderByUserInput(graphene.InputObjectType):
  # id | username | role | isActive | email
  column = graphene.String() # column: String
  # asc | desc
  order = graphene.String() # order: String


# TODO: implement
class FilterUserInput(graphene.InputObjectType):
    # search by username or email
    searchText = graphene.String() # searchText: String
    # filter by role
    role = graphene.String() # role: String
    # filter by isActive
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
    certificate = graphene.Field(AuthCertificateInput) #certificate: AuthCertificateInput
    facebook = graphene.Field(AuthFacebookInput) #facebook: AuthFacebookInput
    google = graphene.Field(AuthGoogleInput) #google: AuthGoogleInput
    github = graphene.Field(AuthGitHubInput) #github: AuthGitHubInput
    linkedin = graphene.Field(AuthLinkedInInput) #linkedin: AuthLinkedInInput


class ProfileInput(graphene.InputObjectType):
    firstName = graphene.String()
    lastName = graphene.String()


class AddUserInput(graphene.InputObjectType):
    username = graphene.String(required=True) # username: String!
    email = graphene.String(required=True) # email: String!
    password = graphene.String(required=True) # password: String!
    role = graphene.String(required=True) # role: String!
    isActive = graphene.Boolean() # isActive: Boolean
    profile = graphene.Field(ProfileInput) # profile: ProfileInput
    auth = graphene.Field(AuthInput) # auth: AuthInput


class EditUserInput(graphene.InputObjectType):
    id = graphene.Int(required=True) #id: Int!
    username = graphene.String() #username: String!
    role = graphene.String() #role: String!
    isActive = graphene.Boolean() #isActive: Boolean
    email = graphene.String()  #email: String!
    password = graphene.String() # NOTE: verify this works
    profile = graphene.Field(ProfileInput) # profile: ProfileInput
    auth = graphene.Field(AuthInput) # auth: AuthInput


class UpdateUserPayload(graphene.ObjectType):
    mutation = graphene.String(required=True) #mutation: String!
    node = User #node: User! # TODO: implement


class Query(graphene.ObjectType):
    user = graphene.Field(UserPayload, id=graphene.Int())
    users = graphene.List(UserType)
    current_user = graphene.Field(UserType)

    def resolve_user(self, info, **input):
        try:
            instance = User.objects.get(id=input.get('id'))
            return UserPayload(user=instance)
        except Exception as e:
            return UserPayload(errors=get_errors(e))


    def resolve_users(self, info, **input):
        # orderBy=OrderByUserInput,
        #     filter=FilterUserInput
        # order_by_user_input =
        # filter_user_input =
        # import pdb; pdb.set_trace()
        return User.objects.all() # TODO: modify to use pagination

    def resolve_current_user(self, info, **input):
        if info.context.user.is_anonymous:
            return None
        else:
            return info.context.user


class AddUser(AuthMutation, graphene.Mutation):
    permission_classes = (AllowAny,)

    class Arguments:
        # addUser(input: AddUserInput!): UserPayload!
        input = graphene.Argument(AddUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        if cls.has_permission(context, info, input):
            try:
                add_user_input = input.get('input', {})

                user = User.objects.create_user(**add_user_input)
                return UserPayload(user=user)
            except ValidationError as e:
                return UserPayload(errors=get_field_errors(e))


class EditUser(AuthMutation, graphene.Mutation):
    # permission_classes = (AllowAuthenticated, AllowOwnerOrSuperuser)
    permission_classes = (AllowAuthenticated, )

    class Arguments:
        # editUser(input: EditUserInput!): UserPayload!
        input = graphene.Argument(EditUserInput, required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        if cls.has_permission(User, info, input):
            try:
                with transaction.atomic():
                    edit_user_input = input.get('input', {})

                    user_input = edit_user_input
                    profile_input = edit_user_input.pop('profile', None)
                    auth_input = edit_user_input.pop('auth', None) # TODO: implmenet auth

                    user = get_object(User, user_input.get('id'), User())
                    profile = UserProfile.objects.get_or_create(user=user)

                    import pdb; pdb.set_trace()

                    if user:
                        password = edit_user_input.pop('password')
                        if password: user_instance.set_password(password)

                        user = update_or_create(user, user_input)
                    if profile_instance:
                        profile = update_or_create(profile, profile_input)

                    return UserPayload(user=user)
            except ValidationError as e:
                return UserPayload(errors=get_field_errors(e))
            except DatabaseError as e:
                return UserPayload(errors=get_field_errors(e))


class DeleteUser(AuthMutation, graphene.Mutation):
    permission_classes = (AllowAuthenticated, AllowOwnerOrSuperuser)

    class Arguments:
        # deleteUser(id: Int!): UserPayload!
        id = graphene.Int(required=True)

    Output = UserPayload

    @classmethod
    def mutate(cls, context, info, **input):
        if cls.has_permission(context, info, input):
            try:
                delete_user_input = input.get('input', {})
                instance = get_object(User, delete_user_input.get('id'))

                if instance:
                    user = instance.delete()
                    return UserPayload(user=user)
            except Exception as e:
                return None


class Mutation(graphene.ObjectType):
    # Create new user
    addUser = AddUser.Field()
    # Edit a user
    editUser = EditUser.Field()
    # Delete a user
    deleteUser = DeleteUser.Field()


class UserSubscription(Subscription):
    class Meta:
        serializer_class = UserSerializer
        stream = 'onUsersUpdated'
        # description = 'User Subscription'

class Subscription(graphene.ObjectType):
    # user_subscription = UserSubscription.Field()
    usersUpdated = UserSubscription.Field()
