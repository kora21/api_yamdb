
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Review, Title, Genre, Category, Title
from users.models import User
from .filters import TitleFilter
from .mixins import CreateListViewSet
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    ConfirmationCodeSerializer,
    TokenSerializer,
    UserSerializer
)
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorAdminModeratorOrReadOnly
)
from api_yamdb.settings import EMAIL_DEFAULT_ADDR


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    User.objects.get_or_create(username=username, email=email)
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code',
        f'Confirmation code for {user}:\n{confirmation_code}',
        {EMAIL_DEFAULT_ADDR},
        {email}
    )
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)}, status.HTTP_200_OK)
    return Response('wrong confirmation code', status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=('get', 'patch',),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)
    pagination_class = LimitOffsetPagination


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        return review.comments.order_by('pub_date')

    def perform_create(self, serilizer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        author = self.request.user
        serilizer.save(author=author, review=review)
