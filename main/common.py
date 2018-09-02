import graphene

class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()

    def resolve_field(self, info, **kwargs):
        return self['field'] # NOTE: cannot use dot notation

    def resolve_message(self, info, **kwargs):
        return self['message'] # NOTE: cannot use dot notation
