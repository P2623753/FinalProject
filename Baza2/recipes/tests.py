import os

import django
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from django.test import Client
from .models import Recipe, Ingredient, IngredientInRecipe
from .forms import RecipeForm, IngredientInRecipeForm, IngredientForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baza2.settings')
django.setup()


@pytest.mark.django_db
def test_home_view_status_code(client):
    """Widok home zwraca status 200."""
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_view_template_used(client):
    """Widok home używa szablonu recipes/home.html."""
    url = reverse('home')
    response = client.get(url)
    assert 'recipes/home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_recipe_view_status_code(client):
    """Widok add_recipe zwraca status 200 dla zalogowanego użytkownika."""
    User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('add_recipe')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_recipe_view_template_used(client):
    """Widok add_recipe używa szablonu recipes/add_recipe.html."""
    User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('add_recipe')
    response = client.get(url)
    assert 'recipes/add_recipe.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_recipe_view_redirects_for_anonymous_user(client):
    """Widok add_recipe przekierowuje niezalogowanego użytkownika."""
    url = reverse('add_recipe')
    response = client.get(url)
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


@pytest.mark.django_db
def test_search_view_status_code(client):
    """Widok search zwraca status 200."""
    url = reverse('search')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_view_template_used(client):
    """Widok search używa szablonu recipes/search.html."""
    url = reverse('search')
    response = client.get(url)
    assert 'recipes/search.html' in [t.name for t in response.templates]


@pytest.fixture
def client():
    """Fixture do tworzenia klienta."""
    return Client()


@pytest.fixture
def user():
    """Fixture do tworzenia użytkownika."""
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def ingredient():
    """Fixture do tworzenia składnika."""
    return Ingredient.objects.create(name='mąka')


@pytest.fixture
def cleanup_recipe():
    """Fixture do usuwania testowego przepisu po zakończeniu testu."""
    yield
    Recipe.objects.filter(title='Test Recipe').delete()


@pytest.mark.django_db
def test_add_recipe_view_post(client, user, ingredient, recipe):
    """Test dla widoku dodawania przepisu (POST) z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('add_recipe'), {
        'title': 'Test Recipe',
        'instructions': 'Test Instructions',
        'preparation_time': '30 min',
        'cooking_time': '45 min',
        'number': '2',
        'ingredient': [ingredient.id],
        'amount': [2],
        'unit': ['g']
    })

    assert response.status_code == 302
    assert Recipe.objects.count() == 2


@pytest.mark.django_db
def test_add_recipe_view_get(client, user):
    """Test dla widoku dodawania przepisu (GET) z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('add_recipe'))
    assert response.status_code == 200


@pytest.fixture
def recipe(user):
    """Fixture do tworzenia przepisu."""
    return Recipe.objects.create(
        title='Test Recipe', instructions='Test Instructions',
        preparation_time='30 min', cooking_time='45 min', number='4', author=user
    )


@pytest.mark.django_db
def test_recipe_edit_view_get(client, user, recipe):
    """Test dla widoku edycji przepisu (GET) z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('recipe_edit', args=[recipe.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_edit_view_post_redirect(client, user, recipe, ingredient):
    """Test dla widoku edycji przepisu (POST) i przekierowania po zapisaniu z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('recipe_edit', args=[recipe.id]), {
        'title': 'Updated Recipe',
        'instructions': 'Updated Instructions',
        'preparation_time': '40 min',
        'cooking_time': '50 min',
        'number': '5',
        'ingredient': [ingredient.id],
        'amount': [2],
        'unit': ['kg']
    })
    assert response.status_code == 302
    assert response.url == reverse('my_recipes')


@pytest.mark.django_db
def test_my_recipes_view(client, user, recipe, ingredient):
    """Test dla widoku 'Moje przepisy' z użyciem pytest."""
    IngredientInRecipe.objects.create(recipe=recipe, ingredient=ingredient, amount=1, unit='g')
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('my_recipes'))
    assert response.status_code == 200
    assert 'Test Recipe' in str(response.content)
    assert '30 min' in str(response.content)
    assert '45 min' in str(response.content)
    assert '4' in str(response.content)


@pytest.mark.django_db
def test_home_view(client, user, recipe):
    """Test dla widoku listy przepisów home z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Test Recipe' in str(response.content)


@pytest.mark.django_db
def test_ingredient_list_view_get(client, user):
    """Test dla widoku listy składników (GET) z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('ingredient_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_ingredient_list_view_post(client, user):
    """Test dla widoku listy składników (POST) z użyciem pytest."""
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('ingredient_list'), {'name': 'mąka'})
    assert response.status_code == 302
    assert Ingredient.objects.count() == 1


@pytest.mark.django_db
def test_recipe_form_valid():
    """Test dla prawidłowego formularza przepisu z użyciem pytest."""
    form_data = {
        'title': 'Test Recipe',
        'instructions': 'Test Instructions',
        'preparation_time': '30 min',
        'cooking_time': '45 min',
        'number': '4',
    }
    form = RecipeForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_recipe_form_invalid():
    """Test dla nieprawidłowego formularza przepisu z użyciem pytest."""
    form_data = {
        'title': '',
        'instructions': 'Test Instructions',
        'preparation_time': '30 min',
        'cooking_time': '45 min',
        'number': '4',
    }
    form = RecipeForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_ingredient_in_recipe_form_valid(ingredient):
    """Test dla prawidłowego formularza składnika w przepisie z użyciem pytest."""
    form_data = {
        'ingredient': ingredient.id,
        'amount': 1,
        'unit': 'g'
    }
    form = IngredientInRecipeForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_ingredient_in_recipe_form_invalid():
    """Test dla nieprawidłowego formularza składnika w przepisie z użyciem pytest."""
    form_data = {
        'ingredient': '',
        'amount': 1,
        'unit': 'g'
    }
    form = IngredientInRecipeForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_ingredient_form_valid():
    """Test dla prawidłowego formularza składnika z użyciem pytest."""
    form_data = {'name': 'mąka'}
    form = IngredientForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_ingredient_form_invalid():
    """Test dla nieprawidłowego formularza składnika z użyciem pytest."""
    form_data = {'name': ''}
    form = IngredientForm(data=form_data)
    assert not form.is_valid()
