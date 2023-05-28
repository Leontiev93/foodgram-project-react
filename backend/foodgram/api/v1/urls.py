from rest_framework import routers

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
#from .views import EmailTokenObtainPairView

from .views import (
    IngredientsViewSet,
    TagsViewSet,
    create_token,
#    FollowViewSet,
#    follow,
    UserViewSet,
    RecipesViewSet
)

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review'
# )
# router_v1.register(
# #    r'users/(?P<id>\d+)/subscriptions',
#     'users/subscriptions',
#     FollowViewSet,
#     basename='follow'
# )
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
    RecipesViewSet
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
#    path(r'users/(?P<id>\d+)/subscribe', follow, name="subscribe"),
    path("auth/token/login/", create_token, name="token"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
