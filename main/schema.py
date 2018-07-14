import graphene
import main.users.schema

class Query(main.users.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
