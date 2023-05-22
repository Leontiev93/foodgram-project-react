from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import mixins
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    TagsSerializer,
    CreateTokenSerializer,
    SignUpSerializer,
    UserSerializer,
)
from .permissions import (
    AdminOrReadOnly,
    AdminOrSuperuserOnly,
    AdminModeratorAuthor
)
from tags.models import Tags
from recipes.models import Ingredient, IngredientsToRecipes, Favorited, Recipes
from users.models import User, Follow


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
#    permission_classes = (AdminOrReadOnly,)


# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = (AdminModeratorAuthor,)
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         new_queryset = Review.objects.filter(title=title_id)
#         return new_queryset

#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, pk=title_id)
#         serializer.save(author=self.request.user, title=title)


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (AdminModeratorAuthor,)
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         review_id = self.kwargs.get('review_id')
#         new_queryset = Comment.objects.filter(review=review_id)
#         return new_queryset

#     def perform_create(self, serializer):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, pk=review_id)
#         serializer.save(author=self.request.user, review=review)


# class TitlesViewSet(viewsets.ModelViewSet):
#     permission_classes = (AdminOrReadOnly,)
#     pagination_class = PageNumberPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = ('name', 'year')

#     def get_serializer_class(self):
#         if self.action in ['list', 'retrieve']:
#             return TitleListSerializer
#         return TitleSerializer

#     def get_queryset(self):
#         queryset = Title.objects.all()
#         category = self.request.query_params.get('category')
#         genre = self.request.query_params.get('genre')
#         if genre is not None:
#             queryset = Title.objects.filter(genre__slug=genre)
#             return queryset
#         elif category is not None:
#             queryset = Title.objects.filter(category__slug=category)
#             return queryset
#         return queryset


# class GenreViewSet(mixins.CreateModelMixin,
#                    mixins.ListModelMixin,
#                    mixins.DestroyModelMixin,
#                    viewsets.GenericViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = (AdminOrReadOnly,)
#     pagination_class = PageNumberPagination
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'


# class CategoryViewSet(mixins.CreateModelMixin,
#                       mixins.ListModelMixin,
#                       mixins.DestroyModelMixin,
#                       viewsets.GenericViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (AdminOrReadOnly,)
#     pagination_class = PageNumberPagination
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'


def send_confirmation_code(user):
    """Функция отправки кода подтверждения."""
    confirmation_code = default_token_generator.make_token(user)

    # User.objects.filter(
    #     username=user
    # ).update(confirmation_code=confirmation_code)
    send_mail(
        subject='Код подтверждения',
        message=(
            f'Приветcвую, {user.username}!\n'
            f'Это письмо содержит код подтверждения регистрации:\n'
            f'{confirmation_code}\n'
            f'Чтоб получить токен, отправьте запрос\n'
            'с полями username и confirmation_code на /api/v1/auth/token/.'
        ),
        from_email='code@YaIMDB.example',
        recipient_list=[user.email]
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Получаем код подтверждения на почту."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    first_name = serializer.data['first_name']
    last_name = serializer.data['last_name']
    email = serializer.data['email']
    user, create = User.objects.get_or_create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    """Функция генерации и отправки токена."""
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = get_object_or_404(
        User,
        email=request.data.get('email')
    )
    password = request.data.get('password')
    # if not default_token_generator.check_token(
    #     email, password
    # ):
    #     err = ('Указанный код подтверждения не совпадает '
    #            'с отправленным на email')
    #     return Response(err, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(
        User,
        email=request.data.get('email'),
    )
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'retrieve']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def users_own_profile(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
