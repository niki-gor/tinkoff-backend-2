from functools import lru_cache
from pydantic import SecretStr, BaseSettings


class AppSettings(BaseSettings):
    secret_key: SecretStr
    class Config:
        env_file = ".env"
        

@lru_cache
def app_settings():
    return AppSettings()
