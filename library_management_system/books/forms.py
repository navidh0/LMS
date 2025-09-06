from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'publish_date', 'availability_status', 'publisher', 'category', 'authors']
