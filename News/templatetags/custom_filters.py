from django import template

register = template.Library()


@register.filter(name='censor')
def censor(values):
    list_value = values.lower().split()
    values = values.split()
    bad_words = ['хуй', 'пизда', 'ебать', 'блять', 'пиздец', 'нахуй']
    for i in range(len(list_value) - 1):
        if list_value[i] in bad_words:
            values[i] = '*' * len(values[i])
    return ' '.join(values)