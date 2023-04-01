from functools import lru_cache

from forum.core.settings import AppSettings


@lru_cache
def get_app_settings():
    return AppSettings()