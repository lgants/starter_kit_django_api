from graphene_django import DjangoObjectType
# from graphene_django_subscriptions.subscription import Subscription
from .models import (Post, Comment)
# from .serializers import (CommentSerializer, PostSerializer)

import graphene

class PostType(DjangoObjectType):

    class Meta:
        name = 'Post'
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        name = 'Comment'
        model = Comment


class PostEdges(graphene.ObjectType):
    node = graphene.Field(PostType)
    cursor = graphene.Int()


class PostPageInfo(graphene.ObjectType):
    endCursor = graphene.Int()
    hasNextPage = graphene.Boolean()


class PostsType(graphene.ObjectType):
    totalCount = graphene.Int()
    edges = graphene.List(PostEdges)
    pageInfo = graphene.Field(PostPageInfo)

    class Meta:
        name = 'Posts'

class Query(graphene.ObjectType):
    comment = graphene.Field(CommentType,
                             id=graphene.Int())
    comments = graphene.List(CommentType)

    post = graphene.Field(PostType,
                          id=graphene.Int())
    posts = graphene.List(PostsType,
                          limit=graphene.Int(),
                          after=graphene.Int())

    def resolve_comment(self, info, **kwargs):
        return Comment.objects.all().first()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

    def resolve_post(self, info, **kwargs):
        return Post.objects.all().first()

    def resolve_posts(self, info, **kwargs):
        print("yolo")
        return Post.objects.all()


# class CommentSubscription(Subscription):
#     class Meta:
#         serializer_class = CommentSerializer
#         stream = 'comments'
#
#
# class PostSubscription(Subscription):
#     class Meta:
#         serializer_class = PostSerializer
#         stream = 'posts'
#
#
# class Subscriptions(graphene.ObjectType):
#     comment_subscription = CommentSubscription.Field()
#     post_subscription = PostSubscription.Field()
