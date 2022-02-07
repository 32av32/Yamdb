from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register('titles', views.TitlesApi)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewApi, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', views.CommentApi, basename='comments')
router.register('categories', views.CategoryApi)
router.register('genres', views.GenreApi)
router.register('users', views.UserApi)

urlpatterns = [
    path('users/me/', views.UserMeApi.as_view()),
    path('', include(router.urls)),
    path('auth/email/', views.get_confirmation_code),
    path('auth/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
