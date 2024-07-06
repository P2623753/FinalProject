from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('recipe/new/', views.recipe_new, name='recipe_new'),
    path('recipe_edit/<int:pk>/', views.recipe_edit, name='recipe_edit'),
    path('recipe_delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),
    path('add_comment/<int:recipe_id>/', views.add_comment, name='add_comment')
]
