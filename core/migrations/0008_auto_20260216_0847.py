
from django.contrib.auth.models import User

def create_admin_user(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
