from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates an app admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="Username of the new admin user")
        parser.add_argument('email', type=str, help="Email of the new admin user")
        parser.add_argument('password', type=str, help="Password of the new admin user")

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists'))
            return

        # Create a new user with admin role
        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = User.ADMIN  # Set the role to ADMIN
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created app admin: {username}'))
