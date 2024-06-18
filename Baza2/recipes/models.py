from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


""" klasa reprezentuje przepis kulinarny z tytułem, opisem, autorem i datą utworzenia."""


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField(Recipe, related_name='ingredients')

    def __str__(self):
        return self.name


"""klasa reprezentuje składnik, który może być przypisany do wielu przepisów."""


class Comment(models.Model):
    """ klasa reprezentuje komentarz dodany przez użytkownika do przepisu."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.recipe}'
