from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.TextField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+$')]
    )
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER)
    bio = models.TextField(
        'Biography',
        max_length=200,
        blank=True,
    )

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN or self.is_superuser or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email',
                ],
                name='unique_username_email',
            )
        ]
