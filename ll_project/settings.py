from pathlib import Path
from platformshconfig import Config

BASE_DIR = Path(__file__).resolve().parent.parent

# Default settings
SECRET_KEY = 'django-insecure-placeholder-key'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Platform.sh config
config = Config()

if config.is_valid_platform():
    # Modify defaults safely
    DEBUG = False
    ALLOWED_HOSTS.append('.platformsh.site')

    if config.appDir:
        STATIC_ROOT = Path(config.appDir) / 'static'

    if config.projectEntropy:
        SECRET_KEY = config.projectEntropy

    # DATABASE configuration
    if not config.in_build():
        db_settings = config.credentials('postgresql')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_settings['path'],
                'USER': db_settings['username'],
                'PASSWORD': db_settings['password'],
                'HOST': db_settings['host'],
                'PORT': db_settings['port'],
            }
        }
    else:
        # SQLite fallback during build
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Local development fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
