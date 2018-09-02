import graphene

class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()

    def resolve_field(self, info, **kwargs):
        return self.field

    def resolve_message(self, info, **kwargs):
        return self.message
