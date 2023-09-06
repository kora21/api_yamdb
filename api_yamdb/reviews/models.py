from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User

from api_yamdb.settings import SCORE_MIN, SCORE_MAX


class Genre(models.Model):
    '''Жанр произведений'''
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Category(models.Model):
    '''Категория произведений'''
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Title(models.Model):
    '''Произведения'''
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=1000,
                                   null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        indexes = [models.Index(fields=['year'])]

    def __str__(self):
        return self.name


class Review(models.Model):
    '''Отзывы.'''

    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(SCORE_MAX),
            MinValueValidator(SCORE_MIN)],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'author',
                    'title',
                ],
                name='unique_author_title',
            )
        ]


class Comment(models.Model):
    '''Комментарии к отзывам.'''

    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        null=False
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        null=False
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return self.text
