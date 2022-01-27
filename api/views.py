from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from .models import Titles, Genre, Category, Review, Comment
from .serializers import TitlesListSerializer, TitlesCreateSerializer, ReviewSerializer, CommentSerializer, CategorySerializer, GenreSerializer
from .filters import TitleFilter


class TitlesApi(ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesListSerializer
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_serializer = TitlesListSerializer(instance=Titles.objects.last())
        return Response(response_serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesListSerializer
        return TitlesCreateSerializer


class ReviewListApi(ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = ReviewSerializer

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
    serializer_class = ReviewSerializer


class CommentListApi(ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer

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
    serializer_class = CommentSerializer


class CategoryListApi(ListCreateAPIView):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CategoryDeleteApi(DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class GenreListApi(ListCreateAPIView):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class GenreDeleteApi(DestroyAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
