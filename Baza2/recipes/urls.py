from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
]
