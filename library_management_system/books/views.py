from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import BookForm
from .models import Book, Category
@login_required
def category_list(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admins can manage categories.")
    categories = Category.objects.all()
    return render(request, 'books/category_list.html', { 'categories': categories })

@login_required
def category_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admins can manage categories.")
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        parent_id = request.POST.get('parent')
        parent = None
        if parent_id and parent_id.isdigit():
            parent = Category.objects.filter(pk=int(parent_id)).first()
        if name:
            Category.objects.create(name=name, parent_category=parent)
            messages.success(request, 'Category created.')
            return redirect('category_list')
        messages.error(request, 'Name is required.')
    categories = Category.objects.all()
    return render(request, 'books/category_form.html', { 'categories': categories })

@login_required
def category_delete(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admins can manage categories.")
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')
    return render(request, 'books/category_confirm_delete.html', { 'category': category })
@login_required
def favorites_list(request):
    from .models import FavoriteBook
    fav_books = Book.objects.filter(favoritebook__user=request.user).select_related('publisher', 'category').prefetch_related('authors')
    return render(request, 'books/favorites_list.html', { 'books': fav_books })
from django.http import HttpResponseForbidden


@login_required
def book_list(request):
    books = Book.objects.all().select_related('publisher', 'category').prefetch_related('authors')
    categories = Category.objects.all()

    title_query = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()
    category_id = request.GET.get('category')
    availability = request.GET.get('availability')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    publish_date = request.GET.get('publish_date')

    # Normalize 'None' and empty strings to None
    if category_id in (None, '', 'None'):
        category_id = None
    if availability not in ['available', 'unavailable']:
        availability = None
    if min_price in (None, '', 'None'):
        min_price = None
    if max_price in (None, '', 'None'):
        max_price = None
    if publish_date in (None, '', 'None'):
        publish_date = None

    # Title search
    if title_query:
        books = books.filter(title__icontains=title_query)

    # Author search
    if author_query:
        # Using filter with ManyToManyField
        books = books.filter(authors__full_name__icontains=author_query).distinct()

    # Category filter
    if category_id and str(category_id).isdigit():
        books = books.filter(category_id=int(category_id))

    # Availability filter
    if availability:
        books = books.filter(availability_status=availability)

    # Price filter
    if min_price is not None:
        try:
            float(min_price)
            books = books.filter(price__gte=min_price)
        except (TypeError, ValueError):
            pass
    if max_price is not None:
        try:
            float(max_price)
            books = books.filter(price__lte=max_price)
        except (TypeError, ValueError):
            pass

    # Publish date (exact)
    if publish_date:
        books = books.filter(publish_date=publish_date)

    # Disable pagination: show all (requested)
    books = books.order_by('title')

    # Favorite ids for current user to color buttons
    favorite_ids = set()
    if request.user.is_authenticated:
        from .models import FavoriteBook
        favorite_ids = set(FavoriteBook.objects.filter(user=request.user).values_list('book_id', flat=True))

    context = {
        'books': books,
        'categories': categories,
        'title_query': title_query,
        'author_query': author_query,
        'category_id': category_id,
        'availability': availability,
        'min_price': min_price,
        'max_price': max_price,
        'publish_date': publish_date,
        'page_obj': None,
        'favorite_ids': favorite_ids,
    }
    return render(request, 'books/book_list.html', context)
    
    
@login_required
def toggle_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    from .models import FavoriteBook
    fav, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)
    if not created:
        fav.delete()
        messages.info(request, 'Removed from favorites.')
    else:
        messages.success(request, 'Added to favorites.')
    return redirect('book_list')

@login_required
def book_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admins can create books.")
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_edit(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admins can edit books.")
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admins can delete books.")
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def delete_filtered_books(request):
    if request.method == "POST":
        if not request.user.is_authenticated or request.user.role != 'admin':
            return HttpResponseForbidden("Only admins can perform bulk delete.")
        books = Book.objects.all()

        title_query = request.POST.get('title', '').strip()
        author_query = request.POST.get('author', '').strip()
        category = request.POST.get('category')
        availability = request.POST.get('availability')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if title_query:
            books = books.filter(title__icontains=title_query)
        if author_query:
            books = books.filter(authors__full_name__icontains=author_query).distinct()

        # --- Category ---
        if category and category.isdigit():
            books = books.filter(category_id=int(category))

        # --- Availability ---
        if availability in ['available', 'unavailable']:
            books = books.filter(availability_status=availability)

        # --- Price filtering (safe casting) ---
        if min_price:
            try:
                books = books.filter(price__gte=float(min_price))
            except ValueError:
                pass  # ignore invalid inputs
        if max_price:
            try:
                books = books.filter(price__lte=float(max_price))
            except ValueError:
                pass
        # Dates
        if start_date:
            books = books.filter(publish_date__gte=start_date)
        if end_date:
            books = books.filter(publish_date__lte=end_date)

        # --- Delete ---
        count = books.count()
        books.delete()

        messages.success(request, f"{count} books deleted.")
        return redirect(reverse('book_list'))