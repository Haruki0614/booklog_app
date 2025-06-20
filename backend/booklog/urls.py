# backend/booklog/urls.py

from django.urls import path
from . import views

app_name = 'booklog'

urlpatterns = [
    # 書籍用のURL
    path('', views.BookListView.as_view(), name='book_list'),
    path('detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add/', views.BookCreateView.as_view(), name='book_add'),
    path('edit/<int:pk>/', views.BookUpdateView.as_view(), name='book_edit'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # メモ用のURL
    path('detail/<int:book_pk>/memo/add/', views.MemoCreateView.as_view(), name='memo_add'),
    path('memo/edit/<int:pk>/', views.MemoUpdateView.as_view(), name='memo_edit'),
    path('memo/delete/<int:pk>/', views.MemoDeleteView.as_view(), name='memo_delete'),
]