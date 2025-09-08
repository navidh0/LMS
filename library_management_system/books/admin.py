from django.contrib import admin
from .models import Publisher, Category, Author, Book, FavoriteBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "category", "publish_date", "availability_status", "price")
    list_filter = ("publisher", "category", "availability_status", "publish_date")
    search_fields = ("title", "authors__full_name", "isbn")
    autocomplete_fields = ("authors",)


admin.site.register(Publisher)
admin.site.register(Category)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)

admin.site.register(FavoriteBook)
