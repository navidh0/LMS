from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='home'),                  # Home page: book list
    path('books/', views.book_list, name='book_list'),       # Also accessible via /books
    path('books/add/', views.book_create, name='book_add'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/delete-filtered/', views.delete_filtered_books, name='delete_filtered_books'),
    path('books/<int:pk>/favorite-toggle/', views.toggle_favorite, name='book_favorite_toggle'),
    path('books/favorites/', views.favorites_list, name='favorites_list'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_add'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
