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

    def resolve_node(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        return Post.objects.first()

    def resolve_cursor(self, info, **kwargs):
        return 1


class PostPageInfo(graphene.ObjectType):
    endCursor = graphene.Int()
    hasNextPage = graphene.Boolean()

    def resolve_endCursor(self, info, **kwargs):
        return 10

    def resolve_hasNextPage(self, info, **kwargs):
        return True


class PostsType(graphene.ObjectType):
    totalCount = graphene.Int()
    edges = graphene.List(PostEdges)
    # edges = graphene.Field(PostEdges)
    pageInfo = graphene.Field(PostPageInfo)

    class Meta:
        name = 'Posts'

    def resolve_totalCount(self, info, **kwargs):
        return Post.objects.all().count()

    def resolve_edges(self, info, **kwargs):
        return [PostEdges]

    def resolve_pageInfo(self, info, **kwargs):
        return PostPageInfo


class Query(graphene.ObjectType):
    comment = graphene.Field(CommentType,
                             id=graphene.Int())
    comments = graphene.List(CommentType)

    post = graphene.Field(PostType,
                          id=graphene.Int())
    posts = graphene.Field(PostsType,
                          limit=graphene.Int(),
                          after=graphene.Int())

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
