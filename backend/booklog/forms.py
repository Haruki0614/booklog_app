# backend/booklog/forms.py

from django import forms
from .models import Book, Memo

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'タイトル',
            'author': '著者',
            'published_date': '出版日',
        }

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'content': 'メモ内容',
        }