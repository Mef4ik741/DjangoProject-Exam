from django import forms
from .models import Article, Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок статьи'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'placeholder': 'Текст статьи'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст статьи',
            'category': 'Категория',
            'image': 'Изображение',
            'status': 'Статус',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user and not user.can_moderate_articles():
            self.fields.pop('status', None)
        if not self.instance or not self.instance.pk:
            self.fields.pop('status', None)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        category = cleaned_data.get('category')
        if not title or not content or not category:
            raise forms.ValidationError('Заполните все обязательные поля')
        return cleaned_data
