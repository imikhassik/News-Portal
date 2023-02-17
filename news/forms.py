from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type',
            'title',
            'text',
            'categories',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is None:
            raise ValidationError({
                'title': 'Название не может быть пустым.'
            })

        text = cleaned_data.get('text')
        if len(text) < 20:
            raise ValidationError({
                'text': 'Текст не может быть менее 20 символов.'
            })
        elif text == title:
            raise ValidationError({
                'text': 'Текст не может быть идентичен названию.'
            })

        return cleaned_data
