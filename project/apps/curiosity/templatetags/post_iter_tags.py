from django import template
from project.apps.curiosity.models import Post, PostComment

register = template.Library()


@register.filter
def post_next(object):
    return object.get_previous_by_created_date.__call__().slug

@register.filter
def post_previous(object):
    return object.get_next_by_created_date.__call__().slug

@register.filter
def post_comment_list(object):
    pass