from django.db import models
from django.contrib.auth.models import User


class Time1(models.Model):
    """klasa reprezentuje pełny czas przygotowania"""
    name = models.CharField(max_length=100, verbose_name='Czas przygotowania')

    def __str__(self):
        return self.name


class Time2(models.Model):
    """klasa reprezentuje Czas pieczenia, gotowania lub smażenia"""
    name = models.CharField(max_length=100, verbose_name='Czas pieczenia/gotowania/smażenia')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """klasa reprezentuje składnik, który może być przypisany do wielu przepisów."""
    name = models.CharField(max_length=100, verbose_name='Składnik')

    def __str__(self):
        return self.name


class Number(models.Model):
    """klasa reprezentuje liczbę porcji które można przygotować podążając za danym przepisem"""
    number = models.CharField(max_length=100, verbose_name='Liczba porcji')

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ klasa reprezentuje typy potraw które można wpisać jako słowo kluczowe"""
    CATEGORY_CHOICES = [
        ('słodycze i ciasta', 'Słodycze i ciasta'),
        ('zupy', 'Zupy'),
        ('dania główne', 'Dania główne'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True,  verbose_name='Nazwa tagu')

    def __str__(self):
        return self.name


class Author(models.Model):
    """klasa reprezentuje imię i nazwisko autora"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Imię i nazwisko')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ klasa reprezentuje przepis kulinarny z nazwą, instrukcją, czasami przygotowania i pieczenia, składnikami, liczbą porcji, autorem oraz słowami kluczowymi."""
    title = models.CharField(max_length=100, verbose_name='Nazwa przepisu')
    instructions = models.TextField(verbose_name='Instrukcje')
    time1 = models.CharField(max_length=100, verbose_name='Czas przygotowania')
    time2 = models.CharField(max_length=100, verbose_name='Czas pieczenia/gotowania/smażenia')
    ingredients = models.TextField(verbose_name='Składniki')
    number = models.CharField(max_length=100, verbose_name='Liczba porcji')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Autor')
    tags = models.ManyToManyField(Tag, verbose_name='Tagi')

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ klasa reprezentuje komentarz dodany przez użytkownika do przepisu."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='Przepis')
    text = models.TextField(verbose_name='Treść komentarza')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return f'Komentarz do {self.recipe.name}'
