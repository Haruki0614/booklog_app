from django.db import models

class Book(models.Model):
    title = models.CharField('タイトル', max_length=200)
    author = models.CharField('著者', max_length=100)
    published_date = models.DateField('出版日', null=True, blank=True)
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.title

class Memo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='memos')
    content = models.TextField('メモ内容')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def __str__(self):
        return f"Memo for {self.book.title}"
