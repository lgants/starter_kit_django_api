from types import SimpleNamespace
import re

# from graphql_relay.node.node import from_global_id
#
# def get_object(object_name, relayId, otherwise=None):
#     try:
#         return object_name.objects.get(pk=from_global_id(relayId)[1])
#     except:
#         return otherwise


# NOTE: doen't manually decamelize; use schema = graphene.Schema(query=..., auto_camelcase=True)
# def _camelize(str):
#     s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
#     return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
#
# def camelizeKeys(obj):
#     result = {}
#     for key, value in obj.items():
#         setattr(result, _camelize(key), value)
#     return result
#
#
# def _decamelize(obj):
#     pass
#
#
# def decamelizeKeys(obj):
#     pass


def get_object(model, id, otherwise=None):
    try:
        return model.objects.get(pk=id)
    except model.DoesNotExist:
        return otherwise

def update_or_create(instance, input, exception=['id']):
    if instance:
        [setattr(instance, key, value) for key, value in input.items() if key not in exception]

    instance.full_clean() # NOTE: necessary to raise ValidationError
    # NOTE: elasticsearch must be running as every saved instance must go through elasticsearch
    instance.save()

    return instance

def get_errors(e):
    # transform django errors to redux errors
    # django: {"key1": [value1], {"key2": [value2]}}
    # redux: ["key1", "value1", "key2", "value2"]
    # fields = e.message_dict.keys()
    # messages = ['; '.join(m) for m in e.message_dict.values()]
    # errors = [i for pair in zip(fields, messages) for i in pair]
    # return errors
    # import pdb; pdb.set_trace()
    return e

def get_field_errors(e):
    errors = []

    for field, messages in e.message_dict.items():
        dict = {'field': field, 'message': '; '.join(messages)}
        error = SimpleNamespace(**dict)
        errors.append(error)

    return errors
