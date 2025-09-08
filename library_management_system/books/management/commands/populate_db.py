from django.core.management.base import BaseCommand
from books.models import Author, Category, Publisher, Book
from datetime import date
import random


def generate_isbn(existing: set[str] | None = None) -> str:
    """Generate a unique 13-digit ISBN not in existing."""
    if existing is None:
        existing = set()
    while True:
        candidate = ''.join([str(random.randint(0, 9)) for _ in range(13)])
        if candidate not in existing:
            return candidate


class Command(BaseCommand):
    help = 'Populate database with rich sample authors, categories, publishers, and books'

    def handle(self, *args, **options):
        # --- Authors ---
        authors_list = [
            "J.K. Rowling", "George Orwell", "Agatha Christie", "Isaac Asimov",
            "Haruki Murakami", "Terry Pratchett", "Dan Brown", "Suzanne Collins",
            "Stephen King", "Neil Gaiman"
        ]
        authors = []
        for name in authors_list:
            author, _ = Author.objects.get_or_create(full_name=name)
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f'Created {len(authors)} authors'))

        # --- Categories ---
        categories_list = ["Fiction", "Mystery", "Science Fiction", "Fantasy", "Non-Fiction", "Thriller"]
        categories = []
        for name in categories_list:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

        # --- Publishers ---
        publishers_list = ["Penguin Books", "Bloomsbury", "HarperCollins", "Random House", "Macmillan", "Simon & Schuster"]
        publishers = []
        for name in publishers_list:
            publisher, _ = Publisher.objects.get_or_create(name=name)
            publishers.append(publisher)
        self.stdout.write(self.style.SUCCESS(f'Created {len(publishers)} publishers'))

        # --- Books ---
        book_titles = [
            "Harry Potter and the Sorcerer's Stone", "1984", "Murder on the Orient Express",
            "Foundation", "Kafka on the Shore", "The Hobbit", "Angels & Demons",
            "The Hunger Games", "The Shining", "American Gods", "Harry Potter and the Chamber of Secrets",
            "Animal Farm", "Death on the Nile", "I, Robot", "Norwegian Wood", "Good Omens",
            "Inferno", "Catching Fire", "It", "Coraline"
        ]

        existing_isbns = set(Book.objects.values_list('isbn', flat=True))
        # Create many books including repeated titles with unique ISBNs
        total = 0
        for i in range(100):
            title = random.choice(book_titles) + f" #{i+1}"
            num_authors = random.choice([1, 2])
            book_authors = random.sample(authors, num_authors)
            category = random.choice(categories)
            publisher = random.choice(publishers)
            price = round(random.uniform(10.0, 50.0), 2)
            year = random.randint(1930, 2020)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            publish_date = date(year, month, day)
            availability_status = random.choice(["available", "unavailable"])
            isbn = generate_isbn(existing_isbns)
            existing_isbns.add(isbn)

            book = Book.objects.create(
                title=title,
                isbn=isbn,
                price=price,
                publish_date=publish_date,
                availability_status=availability_status,
                publisher=publisher,
                category=category
            )

            # ✅ Correct: assign authors INSIDE the loop
            for author in book_authors:
                book.authors.add(author)

            book.save()
            total += 1

        self.stdout.write(self.style.SUCCESS(f'Created {total} books'))
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
