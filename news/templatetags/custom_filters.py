from django import template


register = template.Library()


UNDESIRABLE_WORDS = [
    'последний',
]


@register.filter()
def censor(text: str):
    if type(text) is not str:
        raise TypeError
    censored_text = []
    for word in text.split():
        if word in UNDESIRABLE_WORDS:
            censored_text.append(word[0]+''.join(['*' for _ in word]))
        else:
            censored_text.append(word)
    return ' '.join(censored_text)
