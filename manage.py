#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    settings_file = f'case_management.{os.getenv("DJANGO_ENV", "settings")}'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)
    # if os.environ.get('DJANGO_ENV') == 'production':
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_management.production')
    # else:
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_management.settings')
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
