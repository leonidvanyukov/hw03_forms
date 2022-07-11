from django import forms  # type: ignore
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        help_texts = {
            'text': 'Введите текст Вашего нового поста',
            'group': 'Выберете группу Вашего нового поста',
        }
