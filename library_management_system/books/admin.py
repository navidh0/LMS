from django.contrib import admin
from .models import Publisher, Category, Author, Book, FavoriteBook


# Register your models here.                    
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(FavoriteBook)
