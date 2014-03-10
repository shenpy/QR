import json
from datetime import datetime


def answer_as_json(answer):
    all_fields = [ field.name for field in answer._meta.fields ]
    foreignkeys = {'replyer': 'username'}
    non_foreign_fields = ['id', 'text', 'score', 'create_date']
    non_foreign_fields_kv = [(field, _get_field_value(answer, field)) \
                                    for field in non_foreign_fields]
    foreignkey_fields_kv = []
    for field, foreignkey_field in foreignkeys.items():
        new_field_name = '__'.join([field, foreignkey_field])
        foreignkey_object = getattr(answer, field)
        value = getattr(foreignkey_object, foreignkey_field)
        foreignkey_fields_kv.append((new_field_name, value))
    all_fields_dict = dict(foreignkey_fields_kv + non_foreign_fields_kv)
    return json.dumps([all_fields_dict])

def _get_field_value(instance, attr):
    value = getattr(instance, attr)
    if isinstance(value, datetime):
        value = value.strftime('%Y %m %d %H:%M')
        print value
    return value
