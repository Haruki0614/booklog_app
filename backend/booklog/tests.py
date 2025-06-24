# backend/booklog/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Book

# プロジェクトで使われているUserモデルを取得
User = get_user_model()

class BookModelTests(TestCase):
    """
    Bookモデルのテスト
    """
    def setUp(self):
        """
        Bookモデルのテストで使うユーザーを事前に作成
        """
        self.user = User.objects.create_user(username='modeltestuser', password='password')

    def test_book_str(self):
        """
        Bookモデルの__str__メソッドがタイトルを返すことをテスト
        """
        # 必須項目であるuserを指定してBookオブジェクトを作成
        book = Book.objects.create(
            title="テストタイトル", 
            author="テスト著者",
            user=self.user
        )
        self.assertEqual(str(book), "テストタイトル")

class BookViewsTests(TestCase):
    """
    ビューに関するテスト
    """
    def setUp(self):
        """
        各テストメソッドの実行前に呼ばれるセットアップメソッド
        テスト用のユーザーと書籍を作成
        """
        self.user = User.objects.create_user(
            username='viewtestuser', 
            password='testpassword123'
        )
        self.book = Book.objects.create(
            title="テスト用の本",
            author="テストユーザー",
            user=self.user
        )

    def test_book_list_view_for_anonymous_user(self):
        """
        ログインしていないユーザーが書籍一覧ページにアクセスできるかテスト
        """
        url = reverse('booklog:book_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "テスト用の本")
        self.assertFalse(response.context['user'].is_authenticated)

    def test_book_create_view_redirects_for_anonymous_user(self):
        """
        ログインしていないユーザーが書籍登録ページにアクセスするとリダイレクトされるかテスト
        """
        url = reverse('booklog:book_create')
        response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_book_list_view_for_logged_in_user(self):
        """
        ログイン済みのユーザーが書籍一覧ページにアクセスできるかテスト
        """
        self.client.login(username='viewtestuser', password='testpassword123')
        url = reverse('booklog:book_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "テスト用の本")
        self.assertTrue(response.context['user'].is_authenticated)

    def test_book_create_view_for_logged_in_user(self):
        """
        ログイン済みのユーザーが書籍登録ページにアクセスし、書籍を登録できるかテスト
        """
        self.client.login(username='viewtestuser', password='testpassword123')
        
        url = reverse('booklog:book_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        new_book_data = {
            'title': '新しいテストの本',
            'author': 'テストユーザー',
            'published_date': '2025-06-23',
            'description': 'これはテストで作成した本です。'
        }
        response = self.client.post(url, data=new_book_data)
        
        self.assertRedirects(response, reverse('booklog:book_list'))
        self.assertTrue(Book.objects.filter(title='新しいテストの本').exists())