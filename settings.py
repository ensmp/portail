# Django settings for sitebde project.
import os

basepath = os.path.abspath(os.path.dirname(__file__)) + '/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG 

ADMINS = (
     ('Valentin Anjou', 'valentin.anjou@mines-paristech.fr'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'portail',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'
DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = basepath + 'public/media/'

#MEDIA_ROOT = '/home/bde-mines/sitebde/public/media/'
MEDIA_URL = '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = '/Users/thomas/Dev/sitebde/public/media/'
STATIC_ROOT = basepath + 'public/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    basepath + 'public/static/css',
    basepath + 'public/static/js',
    basepath + 'public/static/img',
    basepath + 'public/static/img/trombi',
    basepath + 'public/static/img/admin',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&fpty=o)a@_!0pu$t7fei1k7!ps1ddf(lw7_ofrnk)&_2pa$m3'
SECRET_KEY_UPDATE = 'clefgit'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    basepath+'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'notification',
    'trombi',
    'radiopsl',
    'association',
    'messages',
    'recherche',
    'petitscours',
    'timetable',
    'sondages',
    'bilanmandat',
    'psl',
    'evenement', 
    'minesmarket',
    'minestryofsound',
    'vendome', 
    'bda',
    'mineshake',
    'pr',
    'faq',
    'chat',
    'bde',
    'htc',
    'S3',
    'abatage',
    'entreprise',
    'paindemine',
    'mediamines',
    'objettrouve',
    'freshbox',
    'machines',
    '1y1b',
    #Avatar, pour les avatars de trombi
    'avatar',
    #TinyMCE pour les messages
    'tinymce',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_HOST = "cobra.ensmp.fr"
EMAIL_PORT = 587 
DEFAULT_FROM_EMAIL = "valentin.anjou@mines-paristech.fr"
EMAIL_HOST_USER = "valentin.anjou"

AUTH_PROFILE_MODULE = 'trombi.UserProfile'

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG={
  'theme': "advanced", 
  'remove_linebreaks': False, 
  'convert_urls': False, 
  'width':'100%',
  'height':'300px',
  'paste_auto_cleanup_on_paste' : True,
  'theme_advanced_buttons1' : "formatselect,separator,bold,italic,hr,separator,link,unlink,separator,bullist,numlist,separator,undo,redo,",
  'theme_advanced_buttons2' : "",
  'theme_advanced_buttons3' : ""  ,
  'theme_advanced_blockformats' : "p,h1,h2,h3,blockquote",
  'theme_advanced_toolbar_location' : "top",
  'content_css' : "/media/css/tiny_editor.css" 
}