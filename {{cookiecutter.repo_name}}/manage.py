#!/usr/bin/env python
import sys
import os
from django.core.management import call_command

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="{{ cookiecutter.app_name }}.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "{{ cookiecutter.app_name }}",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def makemigrations():
    call_command("makemigrations", "{{ cookiecutter.app_name }}")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "not enough arguments. arguments available: test, makemigrations"
    command = sys.argv[1].lower()
    if command == "test":
        run_tests(*sys.argv[2:])

    if command == "makemigrations":
        makemigrations()