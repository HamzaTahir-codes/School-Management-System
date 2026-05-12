from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds CSS class to a form field.
    Usage: {{ form.field|add_class:"my-class" }}
    """
    return value.as_widget(attrs={'class': arg})

@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == 'CheckboxInput'

@register.filter(name='is_radio')
def is_radio(field):
    return field.field.widget.__class__.__name__ == 'RadioSelect'

@register.filter(name='is_file')
def is_file(field):
    return field.field.widget.__class__.__name__ in ['FileInput', 'ClearableFileInput']

@register.filter(name='is_textarea')
def is_textarea(field):
    return field.field.widget.__class__.__name__ == 'Textarea'

