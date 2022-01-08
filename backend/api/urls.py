from django.urls import include, path
from rest_framework import routers

from .views import (FollowApiView, IngredientsViewSet, ListFollowViewSet,
                    RecipeViewSet, TagsViewSet)

router = routers.DefaultRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('users/subscriptions/', ListFollowViewSet.as_view(),
         name='subscription'),
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('', include(router.urls)),
]
