from django import template

register = template.Library()


@register.filter
def add_class_and_placeholder(field, attrs):
    class_name = attrs.split(" ")[0]
    placeholder = attrs.split(" ")[1]
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name)),
        "placeholder": placeholder
    })

@register.filter
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })
