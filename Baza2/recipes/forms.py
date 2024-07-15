from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Recipe, Comment, Ingredient, IngredientInRecipe


class CustomUserCreationForm(UserCreationForm):
    """Formularz rejestracji użytkownika z dodatkowym polem email."""
    email = forms.EmailField(required=True)

    class Meta:
        """Metadane dla formularza użytkownika, określające model i pola."""
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Zapisuje nowego użytkownika z dodanym adresem email."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RecipeForm(forms.ModelForm):
    """formularz do tworzenia i aktualizowania instancji Recipe"""

    class Meta:
        """opcje Meta dla RecipeForm"""
        model = Recipe
        fields = ['title', 'instructions', 'preparation_time', 'cooking_time', 'number']

        labels = {
            'title': 'Nazwa przepisu',
            'instructions': 'Instrukcje',
            'preparation_time': 'Czas przygotowania',
            'cooking_time': 'Czas pieczenia/gotowania/smażenia',
            'number': 'Liczba porcji',


        }
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'preparation_time': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cooking_time': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'number': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

        }


class CommentForm(forms.ModelForm):
    """Formularz do dodawania komentarzy do przepisów."""

    class Meta:
        """Metadane dla formularza komentarza, określające model i pole."""
        model = Comment
        fields = ['text']


class IngredientInRecipeForm(forms.ModelForm):
    """Formularz do dodawania składników do przepisu."""
    class Meta:
        model = IngredientInRecipe
        fields = ['ingredient', 'amount', 'unit']


class IngredientForm(forms.ModelForm):
    """Formularz do tworzenia i edytowania składników."""
    class Meta:
        model = Ingredient
        fields = ['name']
