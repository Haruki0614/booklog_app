
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404

from .models import Book, Memo
from .forms import MemoForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

class BookListView(ListView):
    model = Book
    template_name = 'booklog/book_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'booklog/book_detail.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'published_date']
    template_name = 'booklog/book_form.html'
    success_url = reverse_lazy('booklog:book_list')

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'published_date']
    template_name = 'booklog/book_form.html'
    success_url = reverse_lazy('booklog:book_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'booklog/book_confirm_delete.html'
    success_url = reverse_lazy('booklog:book_list')


class MemoCreateView(CreateView):
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
        context['book_pk'] = self.kwargs['book_pk']
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
    template_name = 'booklog/memo_confirm_delete.html'

    def get_success_url(self):
        # メモが紐づく書籍の詳細ページにリダイレクト
        return reverse_lazy('booklog:book_detail', kwargs={'pk': self.object.book.pk})
    


# --- サインアップビュー ---
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # 登録成功後はログインページにリダイレクト
    template_name = 'booklog/signup.html'


# --- 書籍CRUDビュー ---
# LoginRequiredMixin を追加
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'booklog/book_list.html'

    # ログインユーザーの書籍だけを取得する
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).order_by('-created_at')

# LoginRequiredMixin を追加
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'booklog/book_detail.html'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

# LoginRequiredMixin を追加
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'published_date']
    template_name = 'booklog/book_form.html'
    success_url = reverse_lazy('booklog:book_list')

    # フォームが送信されたときに、userフィールドを自動で設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# LoginRequiredMixin を追加
class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'published_date']
    template_name = 'booklog/book_form.html'
    success_url = reverse_lazy('booklog:book_list')

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

# LoginRequiredMixin を追加
class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'booklog/book_confirm_delete.html'
    success_url = reverse_lazy('booklog:book_list')

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)