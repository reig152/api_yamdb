from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet,
                    CategoryViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
