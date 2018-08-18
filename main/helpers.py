# from graphql_relay.node.node import from_global_id
#
# def get_object(object_name, relayId, otherwise=None):
#     try:
#         return object_name.objects.get(pk=from_global_id(relayId)[1])
#     except:
#         return otherwise

def get_object(model, id, otherwise=None):
    try:
        return model.objects.get(pk=id)
    except:
    # except cls._meta.model.DoesNotExist:
    #     return None
        return otherwise

def update_or_create(instance, input, exception=['id']):
    # import pdb; pdb.set_trace()
    if instance:
        [setattr(instance, key, value) for key, value in input.items() if key not in exception]

    # NOTE: elasticsearch must be running as every saved instance must go through elasticsearch
    instance.save()

    return instance

def get_errors(e):
    # transform django errors to redux errors
    # django: {"key1": [value1], {"key2": [value2]}}
    # redux: ["key1", "value1", "key2", "value2"]
    fields = e.message_dict.keys()
    messages = ['; '.join(m) for m in e.message_dict.values()]
    errors = [i for pair in zip(fields, messages) for i in pair]
    return errors
