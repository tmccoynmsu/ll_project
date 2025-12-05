from pathlib import Path
from platformshconfig import Config

BASE_DIR = Path(__file__).resolve().parent.parent
config = Config()

# ... other settings ...

# DATABASE configuration
if config.is_valid_platform():
    DEBUG = False
    ALLOWED_HOSTS.append('.platformsh.site')

    if config.appDir:
        STATIC_ROOT = Path(config.appDir) / 'static'

    if config.projectEntropy:
        SECRET_KEY = config.projectEntropy

    # Only access credentials **at runtime**
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
        # During build, fallback to SQLite so collectstatic works
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Local fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
