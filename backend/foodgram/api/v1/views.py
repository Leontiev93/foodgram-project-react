from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes, parser_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import mixins
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token

from .serializers import (
    IngredientSerializer,
    TagsSerializer,
    CreateTokenSerializer,
    RecipesSerializer,
    FollowSerializer,
    RecipesListSerializer,
    AuthCustomTokenSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserChangePasswordSerializer
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
#    serializer_class = RecipesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['tags', 'author']
    search_fields = ('author',) 

    def get_queryset(self):
        queryset = Recipes.objects.all()
        if self.request.query_params.get('is_favorited') is not None:
            queryset = Recipes.objects.filter(
                id__in=[i.recipes.id for i in Favorited.objects.filter(
                    user=self.request.user.id)]
                )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        # if self.action in ('favorite', 'shopping_cart'):
        #     return RecipeShortSerializer
        if self.action in ('create', 'partial_update'):
            return RecipesSerializer
        return RecipesListSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


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


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'retrieve']
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
#    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=[
            'post',
        ],
        detail=False,
        url_path='set_password',
        permission_classes=[IsAuthenticated],
    )
    def set_password(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'],
            url_path=r'(?P<id>\d+)/subscribe',
            permission_classes=[IsAuthenticated],)
    def follow(self, request, *args, **kwargs):
        user_id = kwargs['id']
        user = get_object_or_404(User, pk=user_id)
        try:
            Follow.objects.create(user_id=request.user.id, author_id=user_id)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            if request.user.id == int(user_id):
                return Response(
                        "ползователь не может быть подписан на сомого себя",
                        status.HTTP_400_BAD_REQUEST)
            return Response(
                f"ползователь {request.user} уже подписан на {user.username}",
                status.HTTP_400_BAD_REQUEST)

    @follow.mapping.delete
    def unfollow(self, request, *args, **kwargs):
        user_id = kwargs['id']
        user = get_object_or_404(User, pk=user_id)
        try:
            get_object_or_404(
               Follow, user_id=request.user.id,
               author_id=user_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            if request.user.id == int(user_id):
                return Response(
                    "ползователь не может быть подписан на сомого себя",
                    status.HTTP_400_BAD_REQUEST)
            return Response(
                f"ползователь {request.user} не подписан на {user.username}",
                status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


@api_view(['POST'])
@parser_classes([parsers.FormParser,
                 parsers.MultiPartParser,
                 parsers.JSONParser,
                 ])
@renderer_classes([renderers.JSONRenderer, ])
def create_token(request):
    serializer = AuthCustomTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    content = {
        'token': token.key,
    }

    return Response(content)


class FollowViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.from_follower.all()
