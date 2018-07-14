from graphene_django import DjangoObjectType
from .models import User
import graphene

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        return User.objects.all()
