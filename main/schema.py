import graphene
import main.users.schema
import main.counters.schema
import main.posts.schema

class RootQuery(
    main.users.schema.Query,
    main.counters.schema.Query,
    main.posts.schema.Query,
    graphene.ObjectType):
    pass

class RootMutation(
    main.counters.schema.Mutation,
    graphene.ObjectType):
    pass


class RootSubscription(
    main.counters.schema.Subscription,
    main.posts.schema.Subscription,
    graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
    subscription=RootSubscription
)
