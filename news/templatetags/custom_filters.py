from django import template


register = template.Library()


UNDESIRABLE_WORDS = [
    'последний',
    'python',
]


@register.filter()
def censor(text: str):
    if type(text) is not str:
        raise ValueError('censor filter only accepts str values')

    for word in UNDESIRABLE_WORDS:
        text = text.replace(word, f"{word[0]}{'*'*(len(word)-1)}")
        word = word.title()
        text = text.replace(word, f"{word[0]}{'*'*(len(word)-1)}")
    return text
