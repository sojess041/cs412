from django import template

register = template.Library()

@register.filter
def get_request_param(request, key):
    return request.GET.get(key)
