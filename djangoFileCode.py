import textwrap


def MANAGE_PY(project):
    return textwrap.dedent('''\
    import os
    import sys

    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{0}.settings")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
    '''.format(project)).strip()


def APP_ADMIN():
    return textwrap.dedent('''\
    from django.contrib import admin

    # Register your models here.
    ''').strip()


def APP_VIEWS():
    return textwrap.dedent('''\
    from django.shortcuts import render

    # Create your views here.
    ''').strip()


def APP_MODELS():
    return textwrap.dedent('''\
    from django.db import models

    # Create your models here.
    ''').strip()


def APP_TESTS():
    return textwrap.dedent('''\
    from django.test import TestCase

    # Create your tests here.''').strip()


def WSGI_PY(project):
    return textwrap.dedent('''\
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{0}.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    '''.format(project)).strip()


def URLS_PY():
    return textwrap.dedent('''\
    from django.conf.urls import patterns, include, url
    from django.contrib import admin

    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'untitled3.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^admin/', include(admin.site.urls)),
    )
    ''').strip()


def SETTINGS_PY(project, app):
    return textwrap.dedent('''\
    """
    Django settings for untitled3 project.

    For more information on this file, see
    https://docs.djangoproject.com/en/1.7/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.7/ref/settings/
    """

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'nb812krd_^=9gzv#rpi@xfyjgdiiy*lv_nw46c)754xrxepwe$'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        '%s',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = '%s.urls'

    WSGI_APPLICATION = '%s.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    DATABASES = {

        'default'  : {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    STATIC_URL = '/static/'

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR,  'templates'),
    )''' % (app, project, project)).strip()
