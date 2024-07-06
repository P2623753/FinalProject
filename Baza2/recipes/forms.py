from .models import Recipe, Comment, Tag
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
    """formularz do tworzenia i aktualizowania instancji Recipe"""
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        """opcje Meta dla RecipeForm"""
        model = Recipe
        fields = ['title', 'instructions', 'time1', 'time2', 'ingredients', 'number', 'tags']
        labels = {
            'title': 'Nazwa przepisu',
            'instructions': 'Instrukcje',
            'time1': 'Czas przygotowania',
            'time2': 'Czas pieczenia/gotowania/smażenia',
            'ingredients': 'Składniki',
            'number': 'Liczba porcji',
            'tags': 'Tagi'

        }
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'time1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'time2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'number': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tags': forms.CheckboxSelectMultiple
        }


class CommentForm(forms.ModelForm):
    """Formularz do dodawania komentarzy do przepisów."""

    class Meta:
        """Metadane dla formularza komentarza, określające model i pole."""
        model = Comment
        fields = ['text']
