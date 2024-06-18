from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeForm, CommentForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def home(request):
    """Wyświetla stronę główną z listą wszystkich przepisów."""
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})


@login_required
def my_recipes(request):
    """Wyświetla stronę z przepisami zalogowanego użytkownika."""
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


@login_required
def add_recipe(request):
    """Umożliwia zalogowanemu użytkownikowi dodanie nowego przepisu."""
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


def recipe_detail(request, pk):
    """Wyświetla szczegóły wybranego przepisu oraz umożliwia dodanie komentarza."""
    recipe = Recipe.objects.get(pk=pk)
    comments = recipe.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'recipes/recipe_detail.html',
                  {'recipe': recipe, 'comments': comments, 'comment_form': comment_form})


def search(request):
    """Umożliwia wyszukiwanie przepisów na podstawie zapytania użytkownika."""
    query = request.GET.get('q')
    if query:
        results = Recipe.objects.filter(title__icontains=query)
    else:
        results = Recipe.objects.none()
    return render(request, 'recipes/search.html', {'results': results})


def register(request):
    """Obsługuje rejestrację nowego użytkownika."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})


@login_required
def profile(request):
    """Wyświetla profil zalogowanego użytkownika."""
    return render(request, 'recipes/profile.html')
