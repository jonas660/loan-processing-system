
from django.contrib.auth.models import User
from django.db import migrations, models  # <-- this is required!

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_previous_migration'),  # replace with your actual previous migration
    ]

    operations = [
        # Example operation:
        migrations.AddField(
            model_name='yourmodel', 
            name='new_field', 
            field=models.CharField(max_length=100, null=True),
        ),
    ]


def create_admin_user(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_previous_migration'),  # adjust to your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='yourmodel',
            name='new_field',
            field=models.CharField(max_length=100, null=True),
        ),
    ]