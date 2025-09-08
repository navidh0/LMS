from django import forms
from django.core.exceptions import ValidationError
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'publish_date', 'availability_status', 'publisher', 'category', 'authors']
        widgets = {
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '').strip()
        if len(isbn) != 13 or not isbn.isdigit():
            raise ValidationError('ISBN must be 13 numeric characters.')
        return isbn
