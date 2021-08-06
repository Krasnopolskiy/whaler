import os

from django.core.exceptions import ImproperlyConfigured


def get_env_settings(setting, default=None):
    """
    Gets settings from OS environment.

    If `default` is set to `None` raises exception in case no setting in environment.
    """
    try:
        return os.environ[setting]
    except KeyError:
        if default:
            return default
        else:
            raise ImproperlyConfigured(f"{setting} is empty")
