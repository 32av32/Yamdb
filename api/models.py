from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE = [
        ('user', _('User')),
        ('moderator', _('Moderator')),
        ('admin', _('Admin')),
    ]
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE, default='user')
    confirmation_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


class Titles(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='titles')
    genre = models.ManyToManyField('Genre', blank=True, related_name='titles')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey('Titles', on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['title', 'author']


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
