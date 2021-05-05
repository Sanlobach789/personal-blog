from django.core.management import BaseCommand

from authapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.get(username='test_admin'):
            super_user = User()
            super_user.username = 'test_admin'
            super_user.email = ''
            super_user.password = 'geekbrains1'
            super_user.save()
