
from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    """ Klasa obsługująca polecenie tworzenia domyślnych tagów"""
    help = 'Create default tags'

    def handle(self, *args, **kwargs):
        """funkcja tworzy domyślne tagi"""
        tags = ['słodycze i ciasta', 'zupy', 'dania główne']
        for tag in tags:
            Tag.objects.get_or_create(name=tag)
        self.stdout.write(self.style.SUCCESS('Successfully created default tags'))
