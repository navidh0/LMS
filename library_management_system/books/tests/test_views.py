from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from books.models import Book, Author, Category, Publisher
from django.db.models import Q

User = get_user_model()

class BookCRUDTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

        self.author = Author.objects.create(full_name='Author One')
        self.category = Category.objects.create(name='Fiction')
        self.publisher = Publisher.objects.create(name='Publisher One')

        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            price=20,
            publish_date='2023-01-01',
            availability_status='available',
            publisher=self.publisher,
            category=self.category
        )
        self.book.authors.add(self.author)

    def test_book_list(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_book_add(self):
        response = self.client.post(reverse('book_add'), {
            'title': 'New Book',
            'isbn': '9876543210123',
            'price': 30,
            'publish_date': '2023-06-01',
            'availability_status': 'available',
            'publisher': self.publisher.id,
            'category': self.category.id,
            'authors': [self.author.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_book_edit(self):
        response = self.client.post(reverse('book_edit', args=[self.book.id]), {
            'title': 'Updated Book',
            'isbn': self.book.isbn,
            'price': 25,
            'publish_date': '2023-01-01',
            'availability_status': 'unavailable',
            'publisher': self.publisher.id,
            'category': self.category.id,
            'authors': [self.author.id]
        })
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.availability_status, 'unavailable')

    def test_book_delete(self):
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


    def test_book_search(self):
        response = self.client.get(reverse('book_list'), {'q': 'Test'})
        self.assertContains(response, 'Test Book')

    def test_book_filter_availability(self):
        response = self.client.get(reverse('book_list'), {'availability': 'available'})
        self.assertContains(response, 'Test Book')

    def test_delete_filtered_books(self):
        # Add another book
        book2 = Book.objects.create(
            title='Second Book',
            isbn='1111111111111',
            price=15,
            publish_date='2023-01-01',
            availability_status='available',
            publisher=self.publisher,
            category=self.category
        )
        book2.authors.add(self.author)

        response = self.client.get(reverse('delete_filtered_books') + '?availability=available')
        self.assertRedirects(response, reverse('book_list'))
        self.assertFalse(Book.objects.filter(availability_status='available').exists())
