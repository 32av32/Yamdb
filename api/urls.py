from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitlesApi, ReviewListApi, ReviewDetailApi, CommentListApi, CommentDetailApi,
                    CategoryListApi, CategoryDeleteApi, GenreListApi, GenreDeleteApi)

router = DefaultRouter()
router.register('titles', TitlesApi)

urlpatterns = [
    path('', include(router.urls)),
    path('titles/<int:title_id>/reviews/', ReviewListApi.as_view()),
    path('titles/<int:title_id>/reviews/<int:pk>/', ReviewDetailApi.as_view()),
    path('titles/<int:title_id>/reviews/<int:review_id>/comments/', CommentListApi.as_view()),
    path('titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/', CommentDetailApi.as_view()),
    path('titles/<int:title_id>/reviews/', ReviewListApi.as_view()),
    path('categories/', CategoryListApi.as_view()),
    path('categories/<slug:slug>/', CategoryDeleteApi.as_view()),
    path('genres/', GenreListApi.as_view()),
    path('genres/<slug:slug>/', GenreDeleteApi.as_view()),
]
