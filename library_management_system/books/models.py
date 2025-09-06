import re
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=200)
    role = models.CharField(
        max_length=50,
        choices=[("member", "Member"), ("admin", "Admin")],
        default="member"
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="books_users",  # <-- add a custom related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="books_users_permissions",  # <-- add a custom related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    def __str__(self):
        return self.username
    


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address= models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publish_date = models.DateField()
    availability_status = models.CharField(max_length=20, choices=[("available", "Available"), ("unavailable", "Unavailable")])
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    