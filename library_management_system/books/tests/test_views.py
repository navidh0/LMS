from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from books.models import Book, Author, Category, Publisher, FavoriteBook
from datetime import date


class BookViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='admin', password='pass', full_name='Admin', role='admin')
        self.member = User.objects.create_user(username='mem', password='pass', full_name='Member', role='member')
        self.publisher = Publisher.objects.create(name='P1')
        self.category = Category.objects.create(name='C1')
        self.author = Author.objects.create(full_name='A1')
        self.book = Book.objects.create(
            title='B1', isbn='1234567890123', price=10, publish_date=date(2020,1,1),
            availability_status='available', publisher=self.publisher, category=self.category
        )
        self.book.authors.add(self.author)

    def test_list_and_filters(self):
        self.client.login(username='mem', password='pass')
        resp = self.client.get(reverse('book_list'), {'title': 'B1'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'B1')
        resp = self.client.get(reverse('book_list'), {'author': 'A1'})
        self.assertContains(resp, 'B1')
        resp = self.client.get(reverse('book_list'), {'category': str(self.category.id)})
        self.assertContains(resp, 'B1')
        resp = self.client.get(reverse('book_list'), {'min_price': '5', 'max_price': '15'})
        self.assertContains(resp, 'B1')
        resp = self.client.get(reverse('book_list'), {'start_date': '2019-01-01', 'end_date': '2021-01-01'})
        self.assertContains(resp, 'B1')

    def test_member_cannot_crud(self):
        self.client.login(username='mem', password='pass')
        # Create
        resp = self.client.post(reverse('book_add'), {})
        self.assertEqual(resp.status_code, 403)
        # Edit
        resp = self.client.post(reverse('book_edit', args=[self.book.id]), {})
        self.assertEqual(resp.status_code, 403)
        # Delete
        resp = self.client.post(reverse('book_delete', args=[self.book.id]), {})
        self.assertEqual(resp.status_code, 403)

    def test_admin_crud(self):
        self.client.login(username='admin', password='pass')
        # Create
        data = {
            'title': 'B2','isbn': '1234567890124','price': 20,'publish_date': '2021-01-01',
            'availability_status': 'available','publisher': self.publisher.id,'category': self.category.id,
            'authors': [self.author.id]
        }
        resp = self.client.post(reverse('book_add'), data)
        self.assertEqual(resp.status_code, 302)
        # Edit
        resp = self.client.post(reverse('book_edit', args=[self.book.id]), {
            'title': 'B1-edit','isbn': '1234567890123','price': 15,'publish_date': '2020-01-01',
            'availability_status': 'unavailable','publisher': self.publisher.id,'category': self.category.id,
            'authors': [self.author.id]
        })
        self.assertEqual(resp.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'B1-edit')
        # Delete
        resp = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_filtered_admin_only(self):
        # member forbidden
        self.client.login(username='mem', password='pass')
        resp = self.client.post(reverse('delete_filtered_books'), {'title': 'B1'})
        self.assertEqual(resp.status_code, 403)
        # admin can delete
        # create another matching book
        self.client.login(username='admin', password='pass')
        b = Book.objects.create(
            title='Another B1', isbn='1234567890125', price=12, publish_date=date(2020,1,2),
            availability_status='available', publisher=self.publisher, category=self.category
        )
        b.authors.add(self.author)
        resp = self.client.post(reverse('delete_filtered_books'), {'title': 'B1'})
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Book.objects.filter(title__icontains='B1').exists())

    def test_favorite_toggle(self):
        self.client.login(username='mem', password='pass')
        resp = self.client.get(reverse('book_favorite_toggle', args=[self.book.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(FavoriteBook.objects.filter(user__username='mem', book=self.book).exists())
        # toggle off
        resp = self.client.get(reverse('book_favorite_toggle', args=[self.book.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(FavoriteBook.objects.filter(user__username='mem', book=self.book).exists())
