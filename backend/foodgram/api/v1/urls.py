from rest_framework import routers

from django.urls import path, include

from .views import (
    IngredientsViewSet,
    TagsViewSet,
    create_token,
    FollowViewSet,
    UserViewSet,
    RecipesViewSet
)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()
router_v1.register(
    'users/subscriptions',
    FollowViewSet,
    basename='follow'
)
router_v1.register(
    'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    'tags',
    TagsViewSet
)
router_v1.register(
    'recipes',
    RecipesViewSet,
    basename='recipes'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path("auth/token/login/", create_token, name="token"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
