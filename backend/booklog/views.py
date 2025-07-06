from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .models import Book, Memo
from .forms import MemoForm, BookForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db.models import Q

class UserBookOwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).order_by('-id')

class UserMemoOwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Memo.objects.filter(book__user=self.request.user)



class BookListView(UserBookOwnerMixin, ListView):
    model = Book
    template_name = 'booklog/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context

class BookDetailView(UserBookOwnerMixin, DetailView):
    model = Book
    template_name = 'booklog/book_detail.html'

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'booklog/book_form.html'
    success_url = reverse_lazy('booklog:book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdateView(UserBookOwnerMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'booklog/book_form.html'
    
    def get_success_url(self):
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.pk})

class BookDeleteView(UserBookOwnerMixin, DeleteView):
    model = Book
    template_name = 'booklog/book_delete.html'
    success_url = reverse_lazy('booklog:book_list')



class MemoCreateView(UserMemoOwnerMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'booklog/memo_form.html'

    # フォームが送信された際の処理
    def form_valid(self, form):
        # URLから書籍のプライマリキー（pk）を取得
        book_pk = self.kwargs['book_pk']
        # pkを元に書籍オブジェクトを取得
        book = get_object_or_404(Book, pk=book_pk)
        
        # フォームのインスタンスに書籍を紐付ける
        form.instance.book = book
        
        return super().form_valid(form)

    # 保存成功後のリダイレクト先
    def get_success_url(self):
        # メモが紐づく書籍の詳細ページにリダイレクト
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.kwargs['book_pk']})
    
    # テンプレートに渡す追加のコンテキスト
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_pk = self.kwargs['book_pk']
        context['book_pk'] = book_pk
        context['book'] = get_object_or_404(Book, pk=book_pk, user=self.request.user)
        return context

class MemoUpdateView(UserMemoOwnerMixin, UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'booklog/memo_form.html'

    def get_success_url(self):
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.book.pk})


class MemoDeleteView(UserMemoOwnerMixin, DeleteView):
    model = Memo
    template_name = 'booklog/memo_delete.html'

    def get_success_url(self):
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.book.pk})

# --- サインアップビュー ---
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # 登録成功後はログインページにリダイレクト
    template_name = 'booklog/signup.html'

def guest_login(request):
    """ゲストユーザーでログインするためのビュー"""
    guest_username = 'guestuser'
    
    # パスワードは固定でも問題ありませんが、念のためランダムなものを設定します。
    # 実際にはこのパスワードでログインすることはありません。
    guest_password = User.objects.make_random_password() 

    # ゲストユーザーが存在しなければ作成し、存在すれば取得します。
    guest_user, created = User.objects.get_or_create(
        username=guest_username,
        defaults={'password': guest_password} # パスワードはハッシュ化されて保存されます
    )

    # ゲストユーザーが新規作成された場合、サンプルデータを追加します。
    if created:
        # サンプル書籍1
        book1 = Book.objects.create(user=guest_user, title='走れメロス', author='太宰治')
        Memo.objects.create(book=book1, content='友情の物語。感動した。')

        # サンプル書籍2
        book2 = Book.objects.create(user=guest_user, title='こころ', author='夏目漱石')
        Memo.objects.create(book=book2, content='先生と私の関係性が興味深い。')
        Memo.objects.create(book=book2, content='人間のエゴイズムについて考えさせられる。')

    # ゲストユーザーでログイン状態にします
    login(request, guest_user)
    
    # ログイン後は書籍一覧ページにリダイレクトします
    return redirect('booklog:book_list')