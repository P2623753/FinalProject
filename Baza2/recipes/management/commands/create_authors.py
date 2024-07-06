from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Author


class Command(BaseCommand):
    """ Klasa reprezentująca polecenie zarządzania umożliwiające utworzenie instancji autora dla wszystkich istniejących instancji użytkowników, jeśli jeszcze nie istnieją."""
    help = 'Create authors for existing users'

    def handle(self, *args, **kwargs):
        """funkcja tworząca instancje autora dla wszystkich istniejących instancji użytkowników, jeśli jeszcze nie istnieją."""
        for user in User.objects.all():
            author, created = Author.objects.get_or_create(user=user, defaults={'name': user.username})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Author created for user: {user.username}'))
            else:
                self.stdout.write(f'Author already exists for user: {user.username}')
