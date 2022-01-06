from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name[:15]


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тега',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Идентификатор тега',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:15]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        null=False,
        verbose_name='Фото рецепта',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты в рецепте',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='tags',
        verbose_name='Теги для рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Приготовление от 1 минуты.'),
        ],
        verbose_name='Время приготовления в минутах',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:2]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингридиент',
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Больше нуля')],
    )

    class Meta:
        verbose_name = 'Ингридиенты'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return 'Ингридиент в рецепте'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег рецепта',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'tag'],
            name='unique_tag_in_recipe',
        )]
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return 'Тег рецепта'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_user_favorite',
        )]
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_user_shopping_list',
        )]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
