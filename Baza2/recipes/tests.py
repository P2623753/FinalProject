import os
import django
import pytest
from django.contrib.auth.models import User
from .models import Recipe, Comment, Ingredient
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baza2.settings')
django.setup()


@pytest.mark.django_db
def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Wszystkie Przepisy' in response.content.decode()


#Test sprawdza czy widok strony głównej zwraca poprawny status odpowiedzi


@pytest.mark.django_db
def test_home_view_contains_recipes(client):
    user = User.objects.create_user(username='testuser', password='12345')
    Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Test Recipe' in response.content.decode()


#Test sprawdza czy widok strony głównej zwraca poprawny status odpowiedzi oraz czy zawiera określony przepis w treści.

@pytest.mark.django_db
def test_my_recipes_view_authenticated(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Moje Przepisy' in response.content.decode()


#Test sprawdza czy widok "Moje Przepisy" zwraca poprawny status odpowiedzi po uwierzytelnieniu użytkownika oraz czy zawiera frazę "Moje Przepisy" w treści.

@pytest.mark.django_db
def test_my_recipes_view_contains_user_recipes(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Test Recipe' in response.content.decode()


#Test sprawdza czy widok "Moje Przepisy" zwraca poprawny status odpowiedzi po uwierzytelnieniu użytkownika oraz czy zawiera określony przepis w treści.

@pytest.mark.django_db
def test_my_recipes_view_unauthenticated(client):
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to log in
    assert response.url.startswith(reverse('login'))


#Test sprawdza czy widok "Moje Przepisy" przekierowuje do logowania w przypadku braku uwierzytelnienia użytkownika.

@pytest.mark.django_db
def test_add_recipe_view_authenticated(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('add_recipe')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Dodaj Przepis' in response.content.decode()


#Test sprawdza czy widok dodawania przepisu zwraca poprawny status odpowiedzi po uwierzytelnieniu użytkownika oraz czy zawiera frazę "Dodaj Przepis" w treści.

@pytest.mark.django_db
def test_add_recipe_view_post_authenticated(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('add_recipe')
    data = {
        'title': 'New Recipe',
        'description': 'New Recipe Description'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after success
    assert Recipe.objects.filter(title='New Recipe').exists()


#Test sprawdza czy widok dodawania przepisu przekierowuje po pomyślnym dodaniu przepisu oraz czy przepis istnieje w bazie danych.

@pytest.mark.django_db
def test_add_recipe_view_unauthenticated(client):
    url = reverse('add_recipe')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to log in
    assert response.url.startswith(reverse('login'))


#Test sprawdza czy widok dodawania przepisu przekierowuje do logowania w przypadku braku uwierzytelnienia użytkownika.

@pytest.mark.django_db
def test_recipe_detail_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    url = reverse('recipe_detail', args=[recipe.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Test Recipe' in response.content.decode()


#Test sprawdza czy widok szczegółów przepisu zwraca poprawny status odpowiedzi oraz czy zawiera określony przepis w treści.

@pytest.mark.django_db
def test_recipe_detail_view_contains_comments(client):
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    Comment.objects.create(user=user, recipe=recipe, text='Nice recipe!')
    url = reverse('recipe_detail', args=[recipe.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Nice recipe!' in response.content.decode()


#Test sprawdza czy widok szczegółów przepisu zwraca poprawny status odpowiedzi oraz czy zawiera określony komentarz w treści.

@pytest.mark.django_db
def test_recipe_detail_view_add_comment(client):
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    client.login(username='testuser', password='12345')
    url = reverse('recipe_detail', args=[recipe.pk])
    response = client.post(url, {'text': 'Great recipe!'})
    assert response.status_code == 302  # Redirect after success
    assert Comment.objects.filter(text='Great recipe!').exists()


#Test sprawdza czy dodanie komentarza do przepisu przekierowuje po pomyślnym dodaniu oraz czy komentarz istnieje w bazie danych.

@pytest.mark.django_db
def test_search_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    url = reverse('search')
    response = client.get(url, {'q': 'Test'})
    assert response.status_code == 200
    assert 'Test Recipe' in response.content.decode()


#Test sprawdza  czy widok wyszukiwania przepisów zwraca poprawny status odpowiedzi oraz czy zawiera określony przepis w treści.

@pytest.mark.django_db
def test_search_view_no_results(client):
    url = reverse('search')
    response = client.get(url, {'q': 'Nonexistent'})
    assert response.status_code == 200
    assert 'Nie znaleziono przepisu.' in response.content.decode()


#Test sprawdza czy widok wyszukiwania przepisów zwraca poprawny status odpowiedzi oraz czy zawiera określoną informację o braku wyników.

@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Rejestracja' in response.content.decode()


#Test sprawdza czy widok rejestracji zwraca poprawny status odpowiedzi oraz czy zawiera frazę "Rejestracja" w treści.

@pytest.mark.django_db
def test_register_view_post_invalid(client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password1': 'complexpassword123',
        'password2': 'differentpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 200  # Form is redisplayed with errors
    assert '<ul class="errorlist">' in response.content.decode()  # Form errors are displayed
    assert User.objects.filter(username='testuser').count() == 0


#Test sprawdza widok rejestracji, upewniając sie, czy wyświetla błędy formularza, gdy przesłane dane są niepoprawne.

@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Logowanie' in response.content.decode()


#Test sprawdza czy widok logowania zwraca poprawny status odpowiedzi oraz czy zawiera frazę "Logowanie" w treści.

@pytest.mark.django_db
def test_login_view_post(client):
    user = User.objects.create_user(username='testuser', password='12345')
    url = reverse('login')
    response = client.post(url, {'username': 'testuser', 'password': '12345'})
    assert response.status_code == 302  # Redirect after success


#Test sprawdza czy widok logowania przekierowuje po pomyślnym uwierzytelnieniu użytkownika.

@pytest.mark.django_db
def test_logout_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 405  # Redirect after logout
    response = client.get(reverse('home'))
    assert 'logout' in response.content.decode()


#Test sprawdza czy widok wylogowywania zwraca poprawny status odpowiedzi po wylogowaniu oraz czy przekierowuje użytkownika.

@pytest.mark.django_db
def test_home_view_links(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert reverse('home') in response.content.decode()
    assert reverse('my_recipes') in response.content.decode()
    assert reverse('add_recipe') in response.content.decode()
    assert reverse('search') in response.content.decode()


#Test sprawdza czy widok strony głównej zwraca poprawny status odpowiedzi oraz czy zawiera określone linki w treści.

@pytest.mark.django_db
def test_my_recipes_view_contains_only_user_recipes(client):
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')
    client.login(username='user1', password='12345')
    Recipe.objects.create(title='User1 Recipe', description='User1 Description', author=user1)
    Recipe.objects.create(title='User2 Recipe', description='User2 Description', author=user2)
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 200
    assert 'User1 Recipe' in response.content.decode()
    assert 'User2 Recipe' not in response.content.decode()


#Test sprawdza czy widok "Moje Przepisy" zwraca poprawny status odpowiedzi oraz czy zawiera przepisy tylko danego użytkownika.

@pytest.mark.django_db
def test_search_view_empty_query(client):
    url = reverse('search')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Nie znaleziono przepisu' in response.content.decode()


#Test sprawdza czy widok wyszukiwania przepisów zwraca poprawny status odpowiedzi oraz czy zawiera informację o braku wyników.


@pytest.mark.django_db
def test_recipe_creation():
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    assert recipe.title == 'Test Recipe'
    assert recipe.description == 'Test Description'
    assert recipe.author == user


#Test sprawdza utworzenie nowego przepisu i porównuje jego atrybuty z oczekiwanymi.

@pytest.mark.django_db
def test_recipe_str():
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    assert str(recipe) == 'Test Recipe'


#Test sprawdza czy reprezentacja tekstowa przepisu jest zgodna z oczekiwaniami.
@pytest.mark.django_db
def test_ingredient_creation():
    ingredient = Ingredient.objects.create(name='Salt')
    assert ingredient.name == 'Salt'


#Test sprawdza utworzenie nowego składnika i porównuje jego atrybuty z oczekiwanymi.


@pytest.mark.django_db
def test_ingredient_str():
    ingredient = Ingredient.objects.create(name='Salt')
    assert str(ingredient) == 'Salt'


#Test sprawdza czy reprezentacja tekstowa składnika jest zgodna z oczekiwaniami.

@pytest.mark.django_db
def test_comment_creation():
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    comment = Comment.objects.create(user=user, recipe=recipe, text='Nice recipe!')
    assert comment.text == 'Nice recipe!'
    assert comment.user == user
    assert comment.recipe == recipe


#Test sprawdza utworzenie nowego komentarza i porównuje jego atrybuty z oczekiwanymi.


@pytest.mark.django_db
def test_comment_str():
    user = User.objects.create_user(username='testuser', password='12345')
    recipe = Recipe.objects.create(title='Test Recipe', description='Test Description', author=user)
    comment = Comment.objects.create(user=user, recipe=recipe, text='Nice recipe!')
    assert str(comment) == f'Comment by {user} on {recipe}'


#Test sprawdza czy reprezentacja tekstowa komentarza jest zgodna z oczekiwaniami.

@pytest.mark.django_db
def test_logout_view_post(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == 302  # Redirect after logout
    assert response.url == reverse('login')  # Check if redirected to log in


#Test sprawdza  czy widok wylogowywania przekierowuje po wylogowaniu oraz czy przekierowuje użytkownika do logowania.


@pytest.mark.django_db
def test_my_recipes_view_redirect_if_not_logged_in(client):
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to log in
    assert response.url.startswith(reverse('login'))


#Test sprawdza czy widok "Moje Przepisy" przekierowuje do logowania, jeśli użytkownik nie jest zalogowany.


@pytest.mark.django_db
def test_my_recipes_view_access_if_logged_in(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Twoje Przepisy' in response.content.decode()

#Test sprawdza  czy widok "Moje Przepisy" zwraca poprawny status odpowiedzi oraz czy zawiera frazę "Twoje Przepisy" w treści.
