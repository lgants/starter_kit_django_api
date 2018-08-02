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



    # def handle_uploaded_file(f):
    #     with open('some/file/name.txt', 'wb+') as destination:
    #         for chunk in f.chunks():
    #             destination.write(chunk)


    # def mutate(self, info, file, **kwargs):
    # def mutate(self, info, files, **kwargs):
    # def mutate(cls, context, info, **input):
    def mutate(self, info, files, **kwargs):
        try:
            for key, f in info.context.FILES.items():
                path = os.path.join(settings.MEDIA_ROOT, f._name)
                with open(path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            # post = get_object(Post, input.get('input').get('id'))
            # if post:
                # import pdb; pdb.set_trace()
                update_or_create(UploadModel(), kwargs.get('input'))
            return self(ok=True)

        except Exception as e:
            return self(ok=False, errors=get_errors(e))



        # for key, f in info.context.FILES.items():
        #     uploaded_filename = "asdf.jpeg"
        #
        #     full_filename = os.path.join(settings.MEDIA_ROOT, uploaded_filename)
        #     fout = open(full_filename, 'wb+')
        #
        #     file_content = ContentFile(f.read())
        #
        #     for chunk in file_content.chunks():
        #         fout.write(chunk)
        #     fout.close()

        # file parameter is key to uploaded file in FILES from context
        # uploaded_files = info.context.FILES["0"]
        # uploaded_files = info.context.FILES.get(files)
        # do something with your file

        return UploadFiles(ok=True)


class Mutation(graphene.ObjectType):
    # uploadFiles = UploadFiles.Field()
    uploadFiles = UploadFiles.Field()
    removeFile = RemoveFile.Field()
