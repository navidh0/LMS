from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='home'),                  # Home page: book list
    path('books/', views.book_list, name='book_list'),       # Also accessible via /books
    path('books/add/', views.book_create, name='book_add'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/delete-filtered/', views.delete_filtered_books, name='delete_filtered_books'),
]
