import graphene
import main.users.schema
import main.counters.schema
import main.posts.schema

class Query(
    main.users.schema.Query,
    main.counters.schema.Query,
    main.posts.schema.Query,
    graphene.ObjectType):
    pass


# class RootSubscription(
#     main.counters.schema.Subscriptions,
#     # main.posts.schema.Subscriptions,
#     graphene.ObjectType):
#     pass


schema = graphene.Schema(
    query=Query,
    # subscription=RootSubscription
)