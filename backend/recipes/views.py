from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Recipe, RecipeIngredients, ShoppingCart
from .permissions import IsAuthorOrAdminPermission
from .serializers import (RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShortRecipeSerializer)
# from ingredients.models import Ingredient
from users.pagination import CustomPageNumberPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeSerializer

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise exceptions.ValidationError('Рецепт уже в избранном.')
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove_from_favorites(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise exceptions.ValidationError(
                'Рецепта нет в избранном, либо он уже удален.'
            )
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в списке покупок.'
                )

            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок, либо он уже удален.'
                )

            shopping_cart = get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe
            )
            shopping_cart.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(
            user=self.request.user
        ).prefetch_related('items__recipe__ingredients')
        recipe_ids = [
            item.recipe.id for cart in shopping_cart
            for item in cart.items.all()
        ]
        buy_list = RecipeIngredients.objects.filter(
            recipe__id__in=recipe_ids
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))
        buy_list_text = 'Список покупок с сайта Foodgram:\n\n'
        for item in buy_list:
            ingredient_name = item['ingredient__name']
            measurement_unit = item['ingredient__measurement_unit']
            total_amount = item['total_amount']
            buy_list_text += (
                f'{ingredient_name}, {total_amount} {measurement_unit}\n')

        response = HttpResponse(buy_list_text, content_type='text/plain')
        filename = 'shopping-list.txt'
        content_disposition = 'attachment; filename={}'.format(filename)
        response['Content-Disposition'] = content_disposition
