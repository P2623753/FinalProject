import os

import django
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Recipe, Author, Tag

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
def test_my_recipes_view_status_code(client):
    """Widok my_recipes zwraca status 200 dla zalogowanego użytkownika."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    client.login(username='testuser', password='12345')
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_my_recipes_view_template_used(client):
    """Widok my_recipes używa szablonu recipes/my_recipes.html."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    client.login(username='testuser', password='12345')
    url = reverse('my_recipes')
    response = client.get(url)
    assert 'recipes/my_recipes.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_recipe_detail_view_status_code(client):
    """Widok recipe_detail zwraca status 200 dla istniejącego przepisu."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    url = reverse('recipe_detail', args=[recipe.id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_detail_view_template_used(client):
    """Widok recipe_detail używa szablonu recipes/recipe_detail.html."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    url = reverse('recipe_detail', args=[recipe.id])
    response = client.get(url)
    assert 'recipes/recipe_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_recipe_view_status_code(client):
    """Widok add_recipe zwraca status 200 dla zalogowanego użytkownika."""
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('add_recipe')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_recipe_view_template_used(client):
    """Widok add_recipe używa szablonu recipes/add_recipe.html."""
    user = User.objects.create_user(username='testuser', password='12345')
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
def test_add_recipe_view_post(client):
    """Widok add_recipe tworzy nowy przepis dla zalogowanego użytkownika."""
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('add_recipe')
    tag = Tag.objects.create(name='Test Tag')
    data = {
        'title': 'New Recipe',
        'instructions': 'New Instructions',
        'time1': '10 min',
        'time2': '20 min',
        'ingredients': 'ingredient1, ingredient2',
        'number': '4',
        'tags': [tag.id],
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_recipe_edit_view_status_code(client):
    """Widok recipe_edit zwraca status 200 dla istniejącego przepisu."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('recipe_edit', args=[recipe.id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_edit_view_template_used(client):
    """Widok recipe_edit używa szablonu recipes/recipe_edit.html."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('recipe_edit', args=[recipe.id])
    response = client.get(url)
    assert 'recipes/recipe_edit.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_recipe_delete_view_status_code(client):
    """Widok recipe_delete zwraca status 200 dla istniejącego przepisu."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('recipe_delete', args=[recipe.pk])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_delete_view_template_used(client):
    """Widok recipe_delete używa szablonu recipes/recipe_delete.html."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('recipe_delete', args=[recipe.pk])
    response = client.get(url)
    assert 'recipes/recipe_delete.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_add_comment_view_status_code(client):
    """Widok add_comment zwraca status 302 dla istniejącego przepisu (przekierowanie)."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('add_comment', args=[recipe.pk])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_comment_view_redirect(client):
    """Widok add_comment przekierowuje na szczegóły przepisu po dodaniu komentarza."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('add_comment', args=[recipe.pk])
    response = client.post(url, {'text': 'Test comment'})
    assert response.status_code == 302
    assert response.url == reverse('recipe_detail', args=[recipe.pk])


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


@pytest.mark.django_db
def test_search_view_with_results(client):
    """Widok search zwraca wyniki wyszukiwania dla zapytania."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    url = reverse('search')
    response = client.get(url, {'q': 'Test'})
    assert recipe.title in response.content.decode()


@pytest.mark.django_db
def test_search_view_returns_correct_results(client):
    """Widok search zwraca odpowiednie wyniki dla podanego zapytania."""
    user = User.objects.create_user(username='testuser', password='12345')
    author = Author.objects.create(user=user, name='testuser')
    recipe = Recipe.objects.create(title='Test Recipe', instructions='Test Instructions', author=author)
    client.login(username='testuser', password='12345')
    url = reverse('search')
    response = client.get(url, {'q': 'Test'})
    assert response.status_code == 200
    assert 'Test Recipe' in response.content.decode()
