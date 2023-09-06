from django.urls import include, path
from rest_framework import routers
from .views import (
    get_confirmation_code,
    get_token,
    UsersViewSet,
    GenreViewSet,
    CategoryViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UsersViewSet, basename='users')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

users_v1 = [
    path('auth/signup/', get_confirmation_code),
    path('auth/token/', get_token),
]

urlpatterns = [
    path('v1/', include(users_v1)),
    path('v1/', include(router_v1.urls)),
]
