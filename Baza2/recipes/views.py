from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .forms import CustomUserCreationForm, IngredientForm, IngredientInRecipeForm
from .forms import RecipeForm, CommentForm
from .models import Recipe, IngredientInRecipe, Ingredient


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
    global ingredient_form
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author:
        return redirect('home')

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            form.save_m2m()

            IngredientInRecipe.objects.filter(recipe=recipe).delete()

            ingredients = request.POST.getlist('ingredient')
            amounts = request.POST.getlist('amount')
            units = request.POST.getlist('unit')
            for i in range(len(ingredients)):
                if ingredients[i] and amounts[i] and units[i]:
                    ingredient = Ingredient.objects.get(id=ingredients[i])
                    amount = amounts[i]
                    unit = units[i]
                    IngredientInRecipe.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount,
                        unit=unit
                    )

            return redirect('my_recipes')
    else:
        form = RecipeForm(instance=recipe)
        ingredient_form = IngredientInRecipeForm()
    return render(request, 'recipes/recipe_edit.html',
                  {'form': form, 'ingredient_form': ingredient_form, 'recipe': recipe})


@login_required
def recipe_delete(request, pk):
    """Usuwa przepis, jeśli użytkownik jest autorem, po potwierdzeniu przez użytkownika."""
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author:
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


@login_required
def my_recipes(request):
    """Wyświetla stronę z przepisami zalogowanego użytkownika."""
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


@login_required
def add_recipe(request):
    """Umożliwia zalogowanemu użytkownikowi dodanie nowego przepisu."""
    global ingredient_form
    if request.method == "POST":
        form = RecipeForm(request.POST)
        print("POST data:", request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()

            ingredients = request.POST.getlist('ingredient')
            amounts = request.POST.getlist('amount')
            units = request.POST.getlist('unit')

            for i in range(len(ingredients)):
                if ingredients[i] and amounts[i] and units[i]:
                    ingredient = Ingredient.objects.get(id=ingredients[i])
                    amount = amounts[i]
                    unit = units[i]
                    IngredientInRecipe.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount,
                        unit=unit
                    )

            return redirect('home')
        else:
            print("Form is not valid. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field} - Error: {error}")
    else:
        form = RecipeForm()
        ingredient_form = IngredientInRecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form, 'ingredient_form': ingredient_form})


def ingredient_list(request):
    """Umożliwia użytkownikowi dodanie nowego składnika"""
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()

    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/ingredient_list.html', {'form': form, 'ingredients': ingredients})
