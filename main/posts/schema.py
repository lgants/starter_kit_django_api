from graphene_django import DjangoObjectType
from graphene_django_subscriptions.subscription import Subscription
from .models import (Post, Comment)
from .serializers import (PostSerializer, CommentSerializer)
from main.helpers import get_object, update_or_create, get_errors

import graphene


class CommentType(DjangoObjectType):
    id = graphene.Int()

    class Meta:
        name = 'Comment'
        model = Comment


class PostInfo(graphene.Interface):
    id = graphene.Int()
    title = graphene.String()
    content = graphene.String()


class PostType(DjangoObjectType):
    comments = graphene.List(CommentType)

    class Meta:
        name = 'Post'
        model = Post
        interfaces = (PostInfo, )

    def resolve_comments(self, info, **kwargs):
        return self.comments.all()


class PostEdges(graphene.ObjectType):
    node = graphene.Field(PostType)
    cursor = graphene.Int()

    def resolve_node(self, info, **kwargs):
        return self

    def resolve_cursor(self, info, **kwargs):
        return self.id


class PostPageInfo(graphene.ObjectType):
    endCursor = graphene.Int()
    hasNextPage = graphene.Boolean()

    def resolve_endCursor(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        # TODO: use correct end cursor
        return Post.objects.all().count()

    def resolve_hasNextPage(self, info, **kwargs):
        return False


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
        # return [PostEdges]
        return Post.objects.all()

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


class AddPostInput(graphene.InputObjectType):
    title = graphene.String(required=True) #title: String!
    content = graphene.String(required=True) #content: String!

class AddPost(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(AddPostInput)

    id = graphene.String()
    title = graphene.String()
    content = graphene.String()
    comments = graphene.List(CommentType)
    # TODO: add error handling

    @classmethod
    def mutate(cls, context, info, **input):
        post = update_or_create(Post(), input.get('input'))
        return cls(title=post.title, content=post.content)


class EditPostInput(graphene.InputObjectType):
    id = graphene.Int(required=True) #id: Int!
    title = graphene.String(required=True) #title: String!
    content = graphene.String(required=True) #content: String!

class EditPost(graphene.Mutation):
    class Arguments:
        input = graphene.Argument(EditPostInput)

    title = graphene.String()
    content = graphene.String()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, context, info, **input):
        try:
            post = get_object(Post, input.get('input').get('id'))
            if post:
                update_or_create(Post(), input.get('input'))
                return cls(title=post.title, content=post.content)
        except ValidationError as e:
            return cls(title=None, content=None, errors=get_errors(e))



#
# class DeletePost(graphene.Mutation):
#     class Arguments:
#         pass
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         pass
#
#
# class AddComment(graphene.Mutation):
#     class Arguments:
#         pass
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         pass
#
#
# class EditComment(graphene.Mutation):
#     class Arguments:
#         pass
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         pass
#
#
# class DeleteComment(graphene.Mutation):
#     class Arguments:
#         pass
#
#     @classmethod
#     def mutate(cls, context, info, **input):
#         pass


class Mutation(graphene.ObjectType):
    addPost = AddPost.Field()
    editPost = EditPost.Field()
    # deletePost = DeletePost.Field()
    # addComment = AddComment.Field()
    # editComment = EditComment.Field()
    # deleteComment = DeleteComment.Field()


class PostSubscription(Subscription):
    class Meta:
        serializer_class = PostSerializer
        stream = 'posts'


class CommentSubscription(Subscription):
    class Meta:
        serializer_class = CommentSerializer
        stream = 'comments'


class Subscription(graphene.ObjectType):
    comment_subscription = CommentSubscription.Field()
    post_subscription = PostSubscription.Field()
