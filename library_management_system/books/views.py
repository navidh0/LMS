from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import BookForm
from .models import Book, Category


@login_required
def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    title_query = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()
    category_id = request.GET.get('category')
    availability = request.GET.get('availability')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Title search
    if title_query:
        books = books.filter(title__icontains=title_query)

    # Author search
    if author_query:
        # Using filter with ManyToManyField
        books = books.filter(authors__full_name__icontains=author_query).distinct()

    # Category filter
    if category_id:
        books = books.filter(category_id=category_id)

    # Availability filter
    if availability in ['available', 'unavailable']:
        books = books.filter(availability_status=availability)

    # Price filter
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)

    context = {
        'books': books,
        'categories': categories,
        'title_query': title_query,
        'author_query': author_query,
        'category_id': category_id,
        'availability': availability,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'books/book_list.html', context)

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def delete_filtered_books(request):
    # Apply same filters as in book_list
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__full_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(publisher__name__icontains=query)
        ).distinct()
    
    availability = request.GET.get('availability')
    if availability:
        books = books.filter(availability_status=availability)
    
    # More filters like price and date if needed
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        books = books.filter(publish_date__gte=start_date)
    if end_date:
        books = books.filter(publish_date__lte=end_date)
    
    count = books.count()
    books.delete()
    
    # Add success message
    messages.success(request, f"{count} book(s) deleted successfully.")
    
    return redirect('book_list')
