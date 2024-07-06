from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Author
from .forms import RecipeForm, CommentForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class RecipeDetailView(DetailView):
    """Wyświetla szczegóły przepisu"""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Umożliwia zalogowanym użytkownikom tworzenie nowego przepisu. """
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_edit.html'


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """ Umożliwia zalogowanym użytkownikom edytowanie istniejącego przepisu."""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_edit.html'


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    """ Umożliwia zalogowanym użytkownikom usunięcie przepisu."""
    model = Recipe
    template_name = 'recipes/recipe_delete.html'
    success_url = reverse_lazy('recipe_list')


def home(request):
    """Wyświetla stronę główną z listą wszystkich przepisów."""
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})


@login_required
def my_recipes(request):
    """Wyświetla stronę z przepisami zalogowanego użytkownika."""
    author, created = Author.objects.get_or_create(user=request.user, name=request.user.username)
    recipes = Recipe.objects.filter(author=author)
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


@login_required
def add_recipe(request):
    """Umożliwia zalogowanemu użytkownikowi dodanie nowego przepisu."""
    if request.method == "POST":
        form = RecipeForm(request.POST)
        print(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            author, created = Author.objects.get_or_create(user=request.user, defaults={'name': request.user.username})
            recipe.author = author
            recipe.save()
            form.save_m2m()
            return redirect('home')
        else:
            print(form.errors)
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
    results = Recipe.objects.filter(title__icontains=query) if query else []
    return render(request, 'recipes/search.html', {'results': results, 'query': query})


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


@login_required
def recipe_new(request):
    """Tworzy nowy przepis na podstawie danych z formularza i przekierowuje do szczegółów przepisu."""
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_edit.html', {'form': form})


@login_required
def recipe_edit(request, pk):
    """Edytuje istniejący przepis, jeśli użytkownik jest autorem, i zapisuje zmiany po zatwierdzeniu formularza."""
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author.user:
        return redirect('home')

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_edit.html', {'form': form, 'recipe': recipe})


@login_required
def recipe_delete(request, pk):
    """Usuwa przepis, jeśli użytkownik jest autorem, po potwierdzeniu przez użytkownika."""
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author.user:
        return redirect('home')

    if request.method == 'POST':
        recipe.delete()
        return redirect('my_recipes')

    return render(request, 'recipes/recipe_delete.html', {'recipe': recipe})


@login_required
def add_comment(request, recipe_id):
    """Dodaje nowy komentarz do przepisu na podstawie danych z formularza i przekierowuje do szczegółów przepisu."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect('recipe_detail', pk=recipe.pk)
    return redirect('recipe_detail', pk=recipe.pk)


