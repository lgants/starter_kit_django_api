import graphene

class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()

    def resole_field(self, info, **kwargs):
        return "error"

    def resole_message(self, info, **kwargs):
        return "message"
