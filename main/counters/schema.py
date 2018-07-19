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


class AddCounter(graphene.Mutation):
    class Arguments:
        amount = graphene.Int()

    amount = graphene.Int()
    # person = graphene.Field(lambda: Person)

    # def mutate(self, info, amount):
    #     print("amoutn", amount)
    #     return AddCounter(amount=amount)
    # @classmethod
    # def mutate_and_get_payload(cls, context, info, **input):
    #     print("yolo")
    #     pass
    @classmethod
    def mutate(cls, context, info, **input):
    # def mutate(cls, _, args, context, info):
        # import pdb; pdb.set_trace()
        amount = input.get('amount')
        counter = Counter.objects.first()
        counter.amount = amount
        counter.save()
        return AddCounter(amount=counter.amount)


class Mutation(graphene.ObjectType):
    add_counter = AddCounter.Field()

# class CounterSubscription(Subscription):
#     class Meta:
#         serializer_class = CounterSerializer
#         stream = 'counters'
#
#
# class Subscriptions(graphene.ObjectType):
#     counter_subscription = CounterSubscription.Field()
