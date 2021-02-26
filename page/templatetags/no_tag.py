from django import template

register = template.Library()

@register.filter
def no_tag(value):
    newValue = value.replace("<b>","")
    newValue = newValue.replace("</b>", "")
    return newValue