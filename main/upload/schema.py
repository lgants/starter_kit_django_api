from graphene_django import DjangoObjectType
# from graphene_django_subscriptions.subscription import Subscription
from .models import Upload as UploadModel
# from .serializers import (PostSerializer, CommentSerializer)
# from main.helpers import get_object, update_or_create, get_errors
import graphene

class Upload(graphene.types.Scalar):
    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value


class FileType(DjangoObjectType):
    id = graphene.Int() #id: Int!
    name = graphene.String() #name: String!
    type = graphene.String() #type: String!
    size = graphene.Int() #size: Int!
    path = graphene.String() #path: String!

    class Meta:
        name = 'File'
        model = UploadModel


class Query(graphene.ObjectType):
    files = graphene.List(FileType)


# class UploadFiles(graphene.Mutation):
#     class Arguments:
#         files = graphene.List(Upload)
#
#     ok = graphene.Boolean()
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         pass


class RemoveFile(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, context, info, **input):
        pass


class UploadFiles(graphene.Mutation):
    class Arguments:
        files = graphene.List(Upload)
        # files = graphene.List(Upload)

    # success = graphene.Boolean()
    ok = graphene.Boolean()

    # def mutate(self, info, file, **kwargs):
    def mutate(self, info, files, **kwargs):
        # file parameter is key to uploaded file in FILES from context
        uploaded_files = info.context.FILES.get(files)
        import pdb; pdb.set_trace()
        # do something with your file

        return UploadFiles(ok=True)


class Mutation(graphene.ObjectType):
    # uploadFiles = UploadFiles.Field()
    uploadFiles = UploadFiles.Field()
    removeFile = RemoveFile.Field()