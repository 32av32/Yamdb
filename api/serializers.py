from abc import ABC

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Titles, Category, Genre, Review, Comment

User = get_user_model()


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


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')


class TokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=100)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs['email'], confirmation_code=attrs['confirmation_code'])
        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

