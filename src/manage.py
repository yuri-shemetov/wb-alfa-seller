#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

from project_settings.settings import DEBUG


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")
    logging.basicConfig(
        format="%(levelname)s [%(asctime)s] - %(message)s",
        level=logging.DEBUG if DEBUG else logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
