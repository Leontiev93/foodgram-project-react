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
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import mixins
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token

from .pagination import CustomPagination
from .filters import RecipeFilter
from .serializers import (
    IngredientSerializer,
    TagsSerializer,
    RecipesSerializer,
    RecipesShortListSerializer,
    ShopingCartSerializer,
    FollowSerializer,
    RecipesListSerializer,
    AuthCustomTokenSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserChangePasswordSerializer
    
)
from .permissions import (
    CreateNewUser,
    AdminOrAuthor
)
from tags.models import Tags
from recipes.models import Ingredient, Favorited, Recipes, ShoppingCart
from users.models import User, Follow


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
#    filter_class = RecipeFilter
#    filter_class = (filters.SearchFilter, )

    permission_classes = (AdminOrAuthor, )
    filterset_fields = ('tags__slug', )
    search_fields = ('tags__slug', )
    # lookup_field = 'tags'

    def get_queryset(self):
        queryset = Recipes.objects.all()
        author = self.request.user
        if self.request.query_params.get('is_favorited') is not None:
            if self.request.query_params.get('is_favorited') == '1':
                temp_queryset = Favorited.objects.filter(
                        user=author).values('recipes_id')
                queryset = queryset.filter(pk__in=temp_queryset)
        if self.request.query_params.get('is_in_shopping_cart') is not None:
            if self.request.query_params.get('is_in_shopping_cart') == '1':
                temp_queryset = ShoppingCart.objects.filter(
                user=author).values('recipes_id')
                queryset = queryset.filter(pk__in=temp_queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipesSerializer
        return RecipesListSerializer

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            if Favorited.objects.filter(user=request.user, recipes__id=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в Избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipes = get_object_or_404(Recipes, pk=pk)
            Favorited.objects.create(user=request.user, recipes=recipes)
            serializer = RecipesListSerializer(recipes)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        
        if Favorited.objects.filter(user=request.user, recipes__id=pk).exists():
            Favorited.objects.filter(user=request.user, recipes__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не добавлен в Избранное'},
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user, recipes__id=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в корзину'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipes = get_object_or_404(Recipes, pk=pk)
            ShoppingCart.objects.create(user=request.user, recipes=recipes)
            serializer = RecipesListSerializer(recipes)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if ShoppingCart.objects.filter(user=request.user, recipes__id=pk).exists():
            ShoppingCart.objects.filter(user=request.user, recipes__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Рецепт не добавлен в корзину'},
            status=status.HTTP_400_BAD_REQUEST
        )
        


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'retrieve']
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (CreateNewUser,)
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
            serializers = FollowSerializer(
                Follow.objects.create(user_id=request.user.id, author_id=user_id),
                context={"request": request})
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
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
        'auth_token': token.key,
    }

    return Response(content, status=status.HTTP_201_CREATED)


class FollowViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.from_follower.all()


class FavoritedViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RecipesShortListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.favorited.all()
# переопределить
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShoppingCartViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ShopingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.shoppingcart.all()