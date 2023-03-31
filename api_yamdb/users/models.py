from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(
        ('email address'),
        blank=True,
        unique=True
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=32,
        choices=CHOICES_ROLE,
        default='user'
    )

    def __str__(self):
        return self.username
