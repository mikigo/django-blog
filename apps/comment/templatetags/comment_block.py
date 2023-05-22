from django import template

from apps.comment.forms import CommentForm
from apps.comment.models import Comment

register = template.Library()


@register.inclusion_tag("comment/block.html")
def comment_block(target):
    context =  {
        "target": target,
        "comment_form": CommentForm(),
        "comment_list": Comment.get_by_target(target),
    }
    return context