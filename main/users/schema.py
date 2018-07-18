from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from .models import (User, UserProfile, AuthCertificate, AuthFacebook, AuthGithub, AuthGoogle, AuthLinkedin)
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
        name = "AuthCertificate"
        model = AuthCertificate

class AuthFacebookType(DjangoObjectType):
    class Meta:
        name = "AuthFacebook"
        model = AuthFacebook

class AuthGithubType(DjangoObjectType):
    class Meta:
        name = "AuthGithub"
        model = AuthGithub

class AuthGoogleType(DjangoObjectType):
    class Meta:
        name = "AuthGoogle"
        model = AuthGoogle

class AuthLinkedinType(DjangoObjectType):
    class Meta:
        name = "AuthLinkedin"
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

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    current_user = graphene.Field(UserType, id=graphene.Int())

    def resolve_current_user(self, info, **kwargs):
        return User.objects.all().first()

    def resolve_user(self, info, **kwargs):
        return User.objects.all().first()

    def resolve_users(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        return User.objects.all()
