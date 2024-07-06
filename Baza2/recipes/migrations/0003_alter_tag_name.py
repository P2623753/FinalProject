# Generated by Django 4.2 on 2024-07-04 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(choices=[('słodycze i ciasta', 'Słodycze i ciasta'), ('zupy', 'Zupy'), ('dania główne', 'Dania główne')], max_length=50, unique=True, verbose_name='Nazwa tagu'),
        ),
    ]