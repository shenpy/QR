import re
import json
from datetime import datetime

from django.core.urlresolvers import reverse

from users.models import User
from questions.models import Tag

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
    return value

def get_help(text):
    #matches = re.finditer('\@(\S+)\s', text)
    matches = re.finditer(ur'\@([\u4e00-\u9fa5_a-zA-Z0-9]+)[^\@]*', text)
    existing_matches = {}
    asked = []
    for matched in matches:
        username = matched.groups()[0]
        try:
            receiver = User.objects.get(username=username)
        except:
            pass
        else:
            asked.append(receiver)
            orig = matched.group()
            url = reverse('users-user', args=(receiver.id,))
            username_with_link = \
                u'@<a href="{0}">{1}</a> '.format(url, receiver.username)
            orig = u'@{0}'.format(username)
            existing_matches[orig] = username_with_link
    for orig, new in existing_matches.iteritems():
        text = text.replace(orig, new)
    return text, asked


def create_tags(text):
    """ create tag from new question description """
    matches = re.finditer(ur'\#([\u4e00-\u9fa5_a-zA-Z0-9]+)\#', text)
    tags = []
    for matched in matches:
        tag_name = matched.groups()[0]
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)
        orig = matched.group()
        tag_label = \
            u'<a class="question-description-tag" href="{0}">{1}</a>'.format(tag.build_url(), tag.name)
        text = text.replace(orig, tag_label)
    return text, tags
