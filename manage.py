#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.test import TestCase
from django.urls import reverse
from myapp.models import CustomUser

import pymysql
pymysql.install_as_MySQLdb()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
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


class SimpleTestCase(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user = CustomUser.objects.create_user(email="test@example.com", password="Test123!")
        self.assertEqual(user.email, "test@example.com")