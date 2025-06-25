from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Book, Memo
from .forms import MemoForm, BookForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'booklog/book_list.html'
    context_object_name = 'books'
    # 1ページに表示する件数を設定
    paginate_by = 5

    def get_queryset(self):
        # ログインユーザーの書籍のみを新しい順に表示
        return Book.objects.filter(user=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡す追加のデータを設定します。
        """
        context = super().get_context_data(**kwargs)
        # 検索後も検索ボックスにキーワードが残るように、キーワードをテンプレートに渡します。
        context['query'] = self.request.GET.get('q', '')
        return context

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'booklog/book_detail.html'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'booklog/book_form.html'
    success_url = reverse_lazy('booklog:book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'booklog/book_form.html'
    
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.pk})

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'booklog/book_delete.html'
    success_url = reverse_lazy('booklog:book_list')

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)


class MemoCreateView(LoginRequiredMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'booklog/memo_form.html'

    # フォームが送信された際の処理
    def form_valid(self, form):
        # URLから書籍のプライマリキー（pk）を取得
        book_pk = self.kwargs['book_pk']
        # pkを元に書籍オブジェクトを取得
        book = get_object_or_404(Book, pk=book_pk, user=self.request.user)
        
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
        context['book_pk'] = self.kwargs['book_pk']
        book = get_object_or_404(Book, pk=self.kwargs['book_pk'], user=self.request.user)
        context['book'] = book
        return context

class MemoUpdateView(UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'booklog/memo_form.html'

    def get_success_url(self):
        # メモが紐づく書籍の詳細ページにリダイレクト
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.book.pk})


class MemoDeleteView(DeleteView):
    model = Memo
    template_name = 'booklog/memo_delete.html'

    def get_success_url(self):
        # メモが紐づく書籍の詳細ページにリダイレクト
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.book.pk})
    


# --- サインアップビュー ---
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # 登録成功後はログインページにリダイレクト
    template_name = 'booklog/signup.html'