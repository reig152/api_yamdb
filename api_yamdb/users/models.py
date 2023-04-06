from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

CHOICES_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


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

    def __str__(self):
        return self.username

    def clean(self):
        if self.username == 'me':
            raise ValidationError('Запрещено использовать me '
                                  'в качестве username!')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

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


class UserConfirmationCode(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code',
        primary_key=True
    )
    confirmation_code = models.CharField(
        max_length=6,
        default=None,
        null=True,
    )
