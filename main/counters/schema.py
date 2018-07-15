from graphene_django import DjangoObjectType
# from graphene_django_subscriptions.subscription import Subscription
from .models import Counter
# from .serializers import CounterSerializer
import graphene

class CounterType(DjangoObjectType):
    class Meta:
        model = Counter

class Query(graphene.ObjectType):
    counter = graphene.Field(CounterType,
                              id=graphene.Int(),
                              amount=graphene.Int())
    counters = graphene.List(CounterType)

    def resolve_counter(self, info, **kwargs):
        id = kwargs.get('id')
        # amount = kwargs.get('amount')
        # import pdb; pdb.set_trace()

        # return Counter.objects.get(pk=id)
        return Counter.objects.all().first()

    def resolve_counters(self, info, **kwargs):
        # import pdb; pdb.set_trace()
        return Counter.objects.all()


# class CounterSubscription(Subscription):
#     class Meta:
#         serializer_class = CounterSerializer
#         stream = 'counters'
#
#
# class Subscriptions(graphene.ObjectType):
#     counter_subscription = CounterSubscription.Field()
