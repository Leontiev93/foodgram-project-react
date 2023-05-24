from rest_framework import routers

from django.urls import path, include

from .views import (
    TagsViewSet,
    create_token,
    signup,
    UserViewSet
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
#     'titles',
#     TitlesViewSet,
#     basename='title'
# )

router_v1.register(
    'tags',
    TagsViewSet
)
# router_v1.register(
#     'categories',
#     CategoryViewSet
# )
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('', include(router_v1.urls)),
    path("auth/token/", create_token, name="token"),
    path("auth/signup/", signup, name="signup"),
]
