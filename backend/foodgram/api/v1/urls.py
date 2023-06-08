from rest_framework import routers

from django.urls import path, include

from .views import (
    IngredientsViewSet,
    TagsViewSet,
    FollowView,
    FollowUserView,
    RecipesViewSet
)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()
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

urlpatterns = [
    path('users/subscriptions/', FollowView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
    path('users/<int:id>/subscribe/', FollowUserView.as_view()),

]
