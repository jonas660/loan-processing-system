python manage.py makemigrations --emptyfrom django.db import migrations
from django.contrib.auth.models import User

def create_admin_user(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_initial'),  # change if your initial migration is different
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
