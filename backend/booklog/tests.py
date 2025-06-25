from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Book, Memo
from datetime import date

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='テストタイトル',
            author='テスト著者',
            published_date=date(2020, 1, 1),
            user=self.user
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), 'テストタイトル')

    def test_book_fields(self):
        self.assertEqual(self.book.author, 'テスト著者')
        self.assertEqual(self.book.published_date, date(2020, 1, 1))
        self.assertEqual(self.book.user, self.user)

class MemoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='memo_user', password='testpass')
        self.book = Book.objects.create(
            title='メモ本',
            author='著者A',
            user=self.user
        )
        self.memo = Memo.objects.create(
            book=self.book,
            content='メモ内容テスト'
        )

    def test_memo_str(self):
        self.assertIn('Memo for', str(self.memo))
        self.assertIn(self.book.title, str(self.memo))

    def test_memo_content(self):
        self.assertEqual(self.memo.content, 'メモ内容テスト')
        self.assertEqual(self.memo.book, self.book)
