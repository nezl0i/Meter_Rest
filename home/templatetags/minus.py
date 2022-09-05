from django import template
from django.conf import settings

register = template.Library()


def subtract(value, arg):
    return value - arg


register.filter('subtract', subtract)
