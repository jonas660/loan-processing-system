#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from django.contrib.auth import get_user_model

# Setup Django environment
django.setup()

User = get_user_model()

# Check if superuser exists, create if it doesn't
if not User.objects.filter(username="admin1").exists():
    print("Creating superuser 'admin1'")
    User.objects.create_superuser(
        username="admin1",
        email="admin1@example.com",
        password="admin1password"
    )
else:
    print("Superuser 'admin1' already exists")



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loanprocessing.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
