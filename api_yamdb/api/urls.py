from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='review'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)
router.register(r'users', views.UserAdminViewSet)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', views.users_me),
    path('v1/', include(router.urls)),
]
