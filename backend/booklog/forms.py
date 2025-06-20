from django import forms
from .models import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['content'] # フォームに表示するのは content フィールドのみ
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}), # 入力欄を少し大きくする
        }
        labels = {
            'content': 'メモ内容',
        }