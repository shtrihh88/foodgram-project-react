from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from users.models import Follow

from .filters import IngredientsFilter, RecipeFilter
from .mixins import RetriveAndListViewSet
from .pagination import CustomPageNumberPaginator
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (AddRecipeSerializer, FavouriteSerializer,
                          FollowSerializer, IngredientsSerializer,
                          ShoppingListSerializer, ShowFollowersSerializer,
                          ShowRecipeFullSerializer, TagsSerializer)


User = get_user_model()


def get_ingredients_list(ingredients_list):
    ingredients_dict = {}
    list_to_buy = []
    if not ingredients_list:
        return 'Корзина не может быть пустой'
    for ingredient in ingredients_list:
        amount = ingredient.amount
        name = ingredient.ingredient.name
        measurement_unit = ingredient.ingredient.measurement_unit
        if name in ingredients_dict:
            ingredients_dict[name]['amount'] += amount
        else:
            ingredients_dict[name] = {
                'meas_un': measurement_unit,
                'amount': amount,
            }
    for key, value in ingredients_dict.items():
        list_to_buy.append(
            f'{key} - {value["amount"]} {value["meas_un"]}.\n',
        )
    return list_to_buy


def download_response(download_list, filename):
    response = HttpResponse(download_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all().order_by('id')
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthorOrAdminOrReadOnly])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=pk)
        try:
            Favorite.objects.get(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(
                'Рецепт уже отсутствует в избранном.',
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, permission_classes=[IsAuthorOrAdminOrReadOnly])
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        bad_request = Response(
            'Рецепт уже отсутствует в списке покупок.',
            status=status.HTTP_400_BAD_REQUEST,
        )
        try:
            try:
                recipe = Recipe.objects.get(id=pk)
            except Recipe.DoesNotExist:
                return bad_request
            shopping_list = ShoppingList.objects.get(
                user=request.user,
                recipe=recipe,
            )
            shopping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShoppingList.DoesNotExist:
            return bad_request

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        )
        list_to_buy = get_ingredients_list(ingredients_list)
        return download_response(list_to_buy, 'Список_покупок.txt')


class FollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        data = {'user': request.user.id, 'author': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        try:
            subscription = Follow.objects.get(user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                'Ошибка отписки',
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListFollowViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShowFollowersSerializer
    pagination_class = CustomPageNumberPaginator

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(following__user=user).exists():
            return User.objects.filter(following__user=user)
        return Response(
            'У Вас нет подписок!',
            status=status.HTTP_400_BAD_REQUEST,
        )
