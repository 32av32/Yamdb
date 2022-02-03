from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (TitlesApi, ReviewListApi, ReviewDetailApi, CommentListApi, CommentDetailApi, CategoryListApi,
                    CategoryDeleteApi, GenreListApi, GenreDeleteApi, UserApi, UserMeApi, get_confirmation_code, TokenObtainPairView)

router = DefaultRouter()
router.register('titles', TitlesApi)
router.register('users', UserApi)

urlpatterns = [
    path('users/me/', UserMeApi.as_view()),
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
    path('auth/email/', get_confirmation_code),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
