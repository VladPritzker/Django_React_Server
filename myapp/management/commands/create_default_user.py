from django.core.management.base import BaseCommand
from myapp.models import User  # Import your custom user model

class Command(BaseCommand):
    help = 'Create a default user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='default_user').exists():
            default_user = User.objects.create_user(
                username='default_user',
                password='default_password',
                email='default_user@example.com'  # Add the email field
            )
            self.stdout.write(self.style.SUCCESS(f'Default user created with ID: {default_user.id}'))
        else:
            self.stdout.write(self.style.SUCCESS('Default user already exists'))
