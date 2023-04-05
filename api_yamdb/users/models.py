from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


def confirmation_code_generate():
    confirmation_code = ''
    for i in range(6):
        num = str(randint(1, 9))
        confirmation_code += num
    return confirmation_code


class CustomUser(AbstractUser):
    email = models.EmailField(
        ('email address'),
        unique=True,
        blank=False
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=32,
        choices=CHOICES_ROLE,
        default='user'
    )
    password = models.CharField(max_length=128, blank=True)
    confirmation_code = models.CharField(
        max_length=6,
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.confirmation_code = confirmation_code_generate()
        super(CustomUser, self).save(*args, **kwargs)

    def is_user(self):
        if self.role == 'user':
            return True
        return False

    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    def is_admin(self):
        if self.role == 'admin':
            return True
        return False
