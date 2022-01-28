from rest_framework import serializers
from datetime import datetime

from .models import Titles, Category, Genre, Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitlesListSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


def max_year(value):
    if value > datetime.now().year:
        raise serializers.ValidationError('This year has not come yet')


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=Genre.objects.all())
    year = serializers.IntegerField(validators=[max_year])

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description', 'genre', 'category')

