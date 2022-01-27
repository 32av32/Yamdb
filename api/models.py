from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Titles(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0)
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


# class GenreTitle(models.Model):
#     title = models.ForeignKey('Titles', on_delete=models.CASCADE, related_name='genre_title')
#     genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='genre_title')


class Review(models.Model):
    title = models.ForeignKey('Titles', on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
