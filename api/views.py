from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     DestroyAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenViewBase

from .models import Titles, Genre, Category, Review, Comment
from . import serializers
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsAdmin, IsUserOrReadOnly, IsModerator
from .utils import send_ccmail, generate_confirmation_code

User = get_user_model()


class TitlesApi(ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitlesListSerializer
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_serializer = serializers.TitlesListSerializer(instance=Titles.objects.last())
        return Response(response_serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitlesListSerializer
        return serializers.TitlesCreateSerializer


class ReviewListApi(ListCreateAPIView):
    pagination_class = PageNumberPagination
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs['title_id'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        title = Titles.objects.get(pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class ReviewDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsUserOrReadOnly, IsAdmin, IsModerator)


class CommentListApi(ListCreateAPIView):
    pagination_class = PageNumberPagination
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        review = Review.objects.get(pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CommentDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsUserOrReadOnly, IsAdmin, IsModerator)


class CategoryListApi(ListCreateAPIView):
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CategoryDeleteApi(DestroyAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreListApi(ListCreateAPIView):
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class GenreDeleteApi(DestroyAPIView):
    serializer_class = serializers.GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class UserApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)


class UserMeApi(RetrieveAPIView, UpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(User, email=self.request.user.email)


class TokenObtainPairView(TokenViewBase):
    serializer_class = serializers.TokenObtainPairSerializer


@api_view(('POST',))
def get_confirmation_code(request):
    serializer = serializers.ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = generate_confirmation_code()
        send_ccmail(email, confirmation_code)

        user, created = User.objects.get_or_create(email=email)
        user.confirmation_code = confirmation_code
        user.save()

        return Response(data={'email': email}, status=status.HTTP_200_OK)
    return Response(data={'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
