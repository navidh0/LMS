# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=200)
    role = models.CharField(
        max_length=50,
        choices=[("member", "Member"), ("admin", "Admin")],
        default="member"
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users_users",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="users_users_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    def __str__(self):
        return self.username
