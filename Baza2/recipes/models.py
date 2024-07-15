from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    """Klasa reprezentująca składnik, który może być przypisany do wielu przepisów."""
    name = models.CharField(max_length=100, verbose_name='Składnik')

    def __str__(self):
        return self.name


class Unit(models.Model):
    """Klasa reprezentująca jednostki miary"""
    UNIT_CHOICES = [
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
        ('l', 'l')
    ]
    name = models.CharField(max_length=2, choices=UNIT_CHOICES, verbose_name='Jednostka miary')

    def __str__(self):
        return self.get_name_display()


class Recipe(models.Model):
    """Klasa reprezentująca przepis kulinarny z nazwą, instrukcją, czasami przygotowania i pieczenia, składnikami, liczbą porcji, autorem oraz słowami kluczowymi."""
    title = models.CharField(max_length=100, verbose_name='Nazwa przepisu')
    instructions = models.TextField(verbose_name='Instrukcje')
    preparation_time = models.CharField(max_length=100, verbose_name='Czas przygotowania')
    cooking_time = models.CharField(max_length=100, verbose_name='Czas pieczenia/gotowania/smażenia')
    number = models.CharField(max_length=100, verbose_name='Liczba porcji')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    ingredients = models.ManyToManyField('Ingredient', through='IngredientInRecipe', verbose_name='Składniki')

    def __str__(self):
        return self.title


class IngredientInRecipe(models.Model):
    """Klasa reprezentująca składnik w przepisie"""
    UNIT_CHOICES = [
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
        ('l', 'l')
    ]
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Ilość', default=1)
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, verbose_name='Jednostka miary')

    def __str__(self):
        return f"{self.ingredient.name} w {self.recipe.title}"


class Comment(models.Model):
    """Klasa reprezentująca komentarz dodany przez użytkownika do przepisu."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='Przepis')
    text = models.TextField(verbose_name='Treść komentarza')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return f'Komentarz do {self.recipe.title}'
