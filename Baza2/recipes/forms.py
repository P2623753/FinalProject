from .models import Recipe, Comment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
    """Formularz do dodawania i edytowania przepisów."""
    class Meta:
        """Metadane dla formularza przepisu, określające model i pola."""
        model = Recipe
        fields = ['title', 'description']


class CommentForm(forms.ModelForm):
    """Formularz do dodawania komentarzy do przepisów."""
    class Meta:
        """Metadane dla formularza komentarza, określające model i pole."""
        model = Comment
        fields = ['text']
