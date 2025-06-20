
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Memo

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
