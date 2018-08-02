from graphene_django import DjangoObjectType
# from graphene_django_subscriptions.subscription import Subscription
from .models import Upload as UploadModel

# from .serializers import (PostSerializer, CommentSerializer)
# from main.helpers import get_object, update_or_create, get_errors
import graphene
import os

from main.helpers import get_object, update_or_create, get_errors

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.conf import settings

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

    def resolve_files(self, info, **kwargs):
        return UploadModel.objects.all()


class RemoveFile(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, context, info, **input):
        pass


class UploadFiles(graphene.Mutation):
    class Arguments:
        # files = graphene.List(Upload)
        files = graphene.Argument(graphene.List(Upload))

    # success = graphene.Boolean()
    ok = graphene.Boolean()

    # def mutate(self, info, file, **kwargs):
    # def mutate(cls, context, info, **input):
    # @classmethod
    # @classmethod
    def mutate(self, info, files, **kwargs):
        try:
            for key, f in info.context.FILES.items():
                path = os.path.join(settings.MEDIA_ROOT, f.name)
                with open(path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

                # UploadModel.objects.create(name=f.name, type=f.content_type, size=f.size, path=path)
            return UploadFiles(ok=True)
        except Exception as e:
            # return self(ok=False, errors=get_errors(e))
            return UploadFiles(ok=False)


class Mutation(graphene.ObjectType):
    uploadFiles = UploadFiles.Field()
    removeFile = RemoveFile.Field()
