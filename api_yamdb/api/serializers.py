from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment, Genre, Category, Title
from users.models import User


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        required=True,
        max_length=150
    )

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            if User.objects.filter(email=data['email']).exists():
                return data
            raise serializers.ValidationError('username already exist')
        else:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email already exist')
            return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Using "me" for username prohibited'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio'
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    '''Сериализатор модели Title для чтения данных'''
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    '''Сериализатор модели Title для записи данных'''
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор отзывов для остального'''
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if not data:
            raise serializers.ValidationError(
                'Запрос содержит некорректные данные'
            )
        user = self.context['request'].user
        title_id = (
            self._context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(author=user, title=title).exists():
            raise serializers.ValidationError(
                'Нельзя побликовать больше одного отзыва на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор комментариев.'''
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
