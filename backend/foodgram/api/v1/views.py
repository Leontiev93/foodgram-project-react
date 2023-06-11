from rest_framework.pagination import (
    LimitOffsetPagination)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import mixins, ListAPIView

from .pagination import CustomPagination
from .filters import RecipesFilter, IngredientFilter
from .serializers import (
    IngredientSerializer,
    TagsSerializer,
    RecipesSerializer,
    RecipesShortListSerializer,
    ShopingCartSerializer,
    FollowSerializer,
    RecipesListSerializer,
)
from .permissions import AdminOrAuthor
from tags.models import Tags
from recipes.models import Ingredient, Favorited, Recipes, ShoppingCart
from users.models import User, Follow


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    pagination_class = CustomPagination
    filter_class = (RecipesFilter,)
    filter_backends = [DjangoFilterBackend, ]
    permission_classes = (AdminOrAuthor, )
    filterset_fields = ('tags__slug',)

    def get_queryset(self):
        queryset = Recipes.objects.all()
        author = self.request.user
        tags = self.request.query_params.getlist('tags')
        slug_id_list = []
        if self.request.query_params.get('is_favorited') == '1':
            temp_queryset = Favorited.objects.filter(
                user=author).values('recipes_id')
            queryset = queryset.filter(pk__in=temp_queryset)
        if self.request.query_params.get('is_in_shopping_cart') == '1':
            temp_queryset = ShoppingCart.objects.filter(
                user=author).values('recipes_id')
            queryset = queryset.filter(pk__in=temp_queryset)
        if tags:
            for tag in tags:
                ([slug_id_list.append(i.pk)
                    for i in Tags.objects.filter(slug=tag)])
            queryset = queryset.filter(tags__pk__in=slug_id_list)
        return self.filter_queryset(queryset).distinct()

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
            if Favorited.objects.filter(
                    user=request.user, recipes__id=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в Избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipes = get_object_or_404(Recipes, pk=pk)
            Favorited.objects.create(user=request.user, recipes=recipes)
            serializer = RecipesListSerializer(recipes)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if Favorited.objects.filter(
                user=request.user, recipes__id=pk).exists():
            Favorited.objects.filter(
                user=request.user, recipes__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не добавлен в Избранное'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    user=request.user, recipes__id=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в корзину!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipes = get_object_or_404(Recipes, pk=pk)
            ShoppingCart.objects.create(user=request.user, recipes=recipes)
            serializer = RecipesListSerializer(recipes)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if ShoppingCart.objects.filter(
                user=request.user, recipes__id=pk).exists():
            ShoppingCart.objects.filter(
                user=request.user, recipes__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не добавлен в корзину'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['get', ], detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        name_recipe = "recipes__ingredients__recipes__name"
        name_ingredient = "recipes__ingredients__ingredient__name"
        meas_unit = "recipes__ingredients__ingredient__measurement_unit"
        amount = "recipes__ingredients__amount"
        grocery_list = (user.shoppingcart.order_by(
            name_ingredient).values(
            name_recipe,
            name_ingredient,
            meas_unit,
            amount
        ))
        count = 0
        arr = f'Список покупок для {user.get_full_name()} \n\n'
        for prod in grocery_list:
            count += 1
            arr += (
                f'№ {count}  '
                f'{prod[name_ingredient]}-'
                f'{prod[meas_unit]}'
                f' {prod[amount]}\n\n'
            )
        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(arr, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AdminOrAuthor,)
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class FollowView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user.from_follower.all()


class FollowUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.from_follower.filter(author=author).exists():
            return Response(
                f"ползователь {request.user} уже подписан на {author}",
                status.HTTP_400_BAD_REQUEST)
        serializers = FollowSerializer(
            Follow.objects.create(
                user=request.user, author=author),
            context={"request": request}
        )
        return Response(
            data=serializers.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.from_follower.filter(author=author).exists():
            request.user.from_follower.filter(
                author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            f"ползователь {request.user} "
            f"не подписан на {request.user.username}",
            status.HTTP_400_BAD_REQUEST
        )


class FavoritedViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = RecipesShortListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.favorited.all()


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ShopingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.shoppingcart.all()
