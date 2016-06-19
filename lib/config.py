import os


def create_app(env):
    if env == 'local':
        os.environ["DJANGO_SETTINGS_MODULE"] = "cars.settings"
    if env == 'prod':
        os.environ["DJANGO_SETTINGS_MODULE"] = "cars.settings"

    import django
    django.setup()
