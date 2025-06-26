from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import Book, Memo
from .forms import BookForm, MemoForm


class BookModelTest(TestCase):
    """Book モデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_book_creation(self):
        """書籍の作成テスト"""
        book = Book.objects.create(
            title='テスト書籍',
            author='テスト著者',
            published_date=date(2024, 1, 1),
            user=self.user
        )
        
        self.assertEqual(book.title, 'テスト書籍')
        self.assertEqual(book.author, 'テスト著者')
        self.assertEqual(book.published_date, date(2024, 1, 1))
        self.assertEqual(book.user, self.user)
        self.assertEqual(str(book), 'テスト書籍')
        
    def test_book_creation_without_published_date(self):
        """出版日なしの書籍作成テスト"""
        book = Book.objects.create(
            title='出版日なし書籍',
            author='著者名',
            user=self.user
        )
        
        self.assertIsNone(book.published_date)
        self.assertEqual(str(book), '出版日なし書籍')
        
    def test_book_timestamps(self):
        """作成日時・更新日時のテスト"""
        book = Book.objects.create(
            title='タイムスタンプテスト',
            author='著者',
            user=self.user
        )
        
        self.assertIsNotNone(book.created_at)
        self.assertIsNotNone(book.updated_at)
        
        # 更新テスト
        original_updated_at = book.updated_at
        book.title = '更新されたタイトル'
        book.save()
        book.refresh_from_db()
        
        self.assertGreater(book.updated_at, original_updated_at)


class MemoModelTest(TestCase):
    """Memo モデルのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.book = Book.objects.create(
            title='メモテスト書籍',
            author='著者',
            user=self.user
        )
        
    def test_memo_creation(self):
        """メモの作成テスト"""
        memo = Memo.objects.create(
            book=self.book,
            content='これはテストメモです。'
        )
        
        self.assertEqual(memo.book, self.book)
        self.assertEqual(memo.content, 'これはテストメモです。')
        self.assertIsNotNone(memo.created_at)
        self.assertEqual(str(memo), f"Memo for {self.book.title}")
        
    def test_memo_related_name(self):
        """書籍からメモへの逆参照テスト"""
        memo1 = Memo.objects.create(
            book=self.book,
            content='メモ1'
        )
        memo2 = Memo.objects.create(
            book=self.book,
            content='メモ2'
        )
        
        self.assertEqual(self.book.memos.count(), 2)
        self.assertIn(memo1, self.book.memos.all())
        self.assertIn(memo2, self.book.memos.all())
        
    def test_memo_cascade_delete(self):
        """書籍削除時のメモのカスケード削除テスト"""
        memo = Memo.objects.create(
            book=self.book,
            content='削除テストメモ'
        )
        
        memo_id = memo.id
        self.book.delete()
        
        with self.assertRaises(Memo.DoesNotExist):
            Memo.objects.get(id=memo_id)


class BookFormTest(TestCase):
    """BookForm のテスト"""
    
    def test_valid_form(self):
        """有効なフォームデータのテスト"""
        form_data = {
            'title': 'フォームテスト書籍',
            'author': 'フォーム著者',
            'published_date': '2024-01-01'
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_form_without_published_date(self):
        """出版日なしのフォームテスト"""
        form_data = {
            'title': '出版日なし書籍',
            'author': '著者名',
            'published_date': ''
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_form_missing_required_fields(self):
        """必須フィールド不足のテスト"""
        form_data = {
            'published_date': '2024-01-01'
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('author', form.errors)


class MemoFormTest(TestCase):
    """MemoForm のテスト"""
    
    def test_valid_memo_form(self):
        """有効なメモフォームのテスト"""
        form_data = {
            'content': 'これは有効なメモ内容です。'
        }
        form = MemoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_empty_memo_form(self):
        """空のメモフォームのテスト"""
        form_data = {
            'content': ''
        }
        form = MemoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


class BookViewTest(TestCase):
    """Book ビューのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        
        self.book1 = Book.objects.create(
            title='ユーザー1の書籍',
            author='著者1',
            user=self.user1
        )
        self.book2 = Book.objects.create(
            title='ユーザー2の書籍',
            author='著者2',
            user=self.user2
        )
        
    def test_book_list_requires_login(self):
        """書籍一覧のログイン必須テスト"""
        response = self.client.get(reverse('booklog:book_list'))
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
    def test_book_list_authenticated(self):
        """認証済みユーザーの書籍一覧テスト"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('booklog:book_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ユーザー1の書籍')
        self.assertNotContains(response, 'ユーザー2の書籍')  # 他ユーザーの書籍は非表示
        
    def test_book_search(self):
        """書籍検索機能のテスト"""
        self.client.login(username='user1', password='pass123')
        
        # 自分の書籍を追加
        Book.objects.create(
            title='Django入門',
            author='Python太郎',
            user=self.user1
        )
        
        # タイトル検索
        response = self.client.get(reverse('booklog:book_list'), {'query': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django入門')
        
        # 著者検索
        response = self.client.get(reverse('booklog:book_list'), {'query': 'Python太郎'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django入門')
        
    def test_book_detail_view(self):
        """書籍詳細ビューのテスト"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('booklog:book_detail', kwargs={'pk': self.book1.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book1.author)
        
    def test_book_detail_other_user_book(self):
        """他ユーザーの書籍詳細アクセステスト"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('booklog:book_detail', kwargs={'pk': self.book2.pk})
        )
        
        self.assertEqual(response.status_code, 404)  # アクセス不可
        
    def test_book_create_get(self):
        """書籍作成フォーム表示テスト"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('booklog:book_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '書籍の登録')
        
    def test_book_create_post(self):
        """書籍作成POSTテスト"""
        self.client.login(username='user1', password='pass123')
        
        form_data = {
            'title': '新しい書籍',
            'author': '新著者',
            'published_date': '2024-01-01'
        }
        
        response = self.client.post(reverse('booklog:book_create'), data=form_data)
        
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertTrue(
            Book.objects.filter(
                title='新しい書籍',
                user=self.user1
            ).exists()
        )
        
    def test_book_update(self):
        """書籍更新テスト"""
        self.client.login(username='user1', password='pass123')
        
        form_data = {
            'title': '更新された書籍',
            'author': '更新された著者',
            'published_date': '2024-12-31'
        }
        
        response = self.client.post(
            reverse('booklog:book_update', kwargs={'pk': self.book1.pk}),
            data=form_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, '更新された書籍')
        self.assertEqual(self.book1.author, '更新された著者')
        
    def test_book_delete(self):
        """書籍削除テスト"""
        self.client.login(username='user1', password='pass123')
        
        book_id = self.book1.pk
        response = self.client.post(
            reverse('booklog:book_delete', kwargs={'pk': book_id})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(id=book_id).exists())


class MemoViewTest(TestCase):
    """Memo ビューのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.book = Book.objects.create(
            title='メモテスト書籍',
            author='著者',
            user=self.user
        )
        self.memo = Memo.objects.create(
            book=self.book,
            content='既存のメモ'
        )
        
    def test_memo_create(self):
        """メモ作成テスト"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'content': '新しいメモ内容です。'
        }
        
        response = self.client.post(
            reverse('booklog:memo_add', kwargs={'book_pk': self.book.pk}),
            data=form_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Memo.objects.filter(
                book=self.book,
                content='新しいメモ内容です。'
            ).exists()
        )
        
    def test_memo_update(self):
        """メモ更新テスト"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'content': '更新されたメモ内容'
        }
        
        response = self.client.post(
            reverse('booklog:memo_edit', kwargs={'pk': self.memo.pk}),
            data=form_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.memo.refresh_from_db()
        self.assertEqual(self.memo.content, '更新されたメモ内容')
        
    def test_memo_delete(self):
        """メモ削除テスト"""
        self.client.login(username='testuser', password='testpass123')
        
        memo_id = self.memo.pk
        response = self.client.post(
            reverse('booklog:memo_delete', kwargs={'pk': memo_id})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Memo.objects.filter(id=memo_id).exists())


class SignUpViewTest(TestCase):
    """サインアップビューのテスト"""
    
    def test_signup_get(self):
        """サインアップフォーム表示テスト"""
        response = self.client.get(reverse('booklog:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '新規登録')
        
    def test_signup_post_success(self):
        """サインアップ成功テスト"""
        form_data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        
        response = self.client.post(reverse('booklog:signup'), data=form_data)
        
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
    def test_signup_password_mismatch(self):
        """パスワード不一致テスト"""
        form_data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'differentpass123'
        }
        
        response = self.client.post(reverse('booklog:signup'), data=form_data)
        
        self.assertEqual(response.status_code, 200)  # フォーム再表示
        self.assertFalse(User.objects.filter(username='newuser').exists())


class UserAuthenticationTest(TestCase):
    """ユーザー認証のテスト"""
    
    def setUp(self):
        """テスト用ユーザーの作成"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_login_success(self):
        """ログイン成功テスト"""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
    def test_login_failure(self):
        """ログイン失敗テスト"""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)  # ログインフォーム再表示
        self.assertContains(response, 'ログイン')


class IntegrationTest(TestCase):
    """統合テスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='integrationuser',
            password='testpass123'
        )
        
    def test_complete_book_workflow(self):
        """書籍の完全なワークフローテスト"""
        # ログイン
        self.client.login(username='integrationuser', password='testpass123')
        
        # 書籍作成
        book_data = {
            'title': '統合テスト書籍',
            'author': '統合著者',
            'published_date': '2024-01-01'
        }
        response = self.client.post(reverse('booklog:book_create'), data=book_data)
        self.assertEqual(response.status_code, 302)
        
        book = Book.objects.get(title='統合テスト書籍')
        
        # 書籍詳細確認
        response = self.client.get(reverse('booklog:book_detail', kwargs={'pk': book.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '統合テスト書籍')
        
        # メモ追加
        memo_data = {
            'content': '統合テストのメモです。'
        }
        response = self.client.post(
            reverse('booklog:memo_add', kwargs={'book_pk': book.pk}),
            data=memo_data
        )
        self.assertEqual(response.status_code, 302)
        
        # メモが追加されたことを確認
        response = self.client.get(reverse('booklog:book_detail', kwargs={'pk': book.pk}))
        self.assertContains(response, '統合テストのメモです。')
        
        # 書籍更新
        updated_data = {
            'title': '更新された統合テスト書籍',
            'author': '統合著者',
            'published_date': '2024-01-01'
        }
        response = self.client.post(
            reverse('booklog:book_update', kwargs={'pk': book.pk}),
            data=updated_data
        )
        self.assertEqual(response.status_code, 302)
        
        # 更新確認
        book.refresh_from_db()
        self.assertEqual(book.title, '更新された統合テスト書籍')
        
        # 検索テスト
        response = self.client.get(reverse('booklog:book_list'), {'query': '更新された'})
        self.assertContains(response, '更新された統合テスト書籍')