# Generated by Django 5.0.6 on 2024-07-03 10:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Składnik')),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, verbose_name='Liczba porcji')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Tagi')),
            ],
        ),
        migrations.CreateModel(
            name='Time1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Czas przygotowania')),
            ],
        ),
        migrations.CreateModel(
            name='Time2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Czas pieczenia/gotowania/smażenia')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Imię i nazwisko')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Nazwa przepisu')),
                ('instructions', models.TextField(verbose_name='Instrukcje')),
                ('time1', models.CharField(max_length=100, verbose_name='Czas przygotowania')),
                ('time2', models.CharField(max_length=100, verbose_name='Czas pieczenia/gotowania/smażenia')),
                ('ingredients', models.TextField(verbose_name='Składniki')),
                ('number', models.CharField(max_length=100, verbose_name='Liczba porcji')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.author', verbose_name='Autor')),
                ('tags', models.ManyToManyField(to='recipes.tag', verbose_name='Tagi')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Treść komentarza')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='recipes.recipe', verbose_name='Przepis')),
            ],
        ),
    ]
