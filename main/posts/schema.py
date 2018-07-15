from graphene_django import DjangoObjectType
# from graphene_django_subscriptions.subscription import Subscription
from .models import (Post, Comment)
# from .serializers import (CommentSerializer, PostSerializer)

import graphene

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    comment = graphene.Field(CommentType, id=graphene.Int())
    comments = graphene.List(CommentType)

    post = graphene.Field(PostType, id=graphene.Int())
    posts = graphene.List(PostType)

    def resolve_comment(self, info, **kwargs):
        return Comment.objects.all().first()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

    def resolve_post(self, info, **kwargs):
        return Post.objects.all().first()

    def resolve_posts(self, info, **kwargs):
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
