from functools import lru_cache
from pydantic import SecretStr, BaseSettings


class AppSettings(BaseSettings):
    secret_key: SecretStr = 'THIS STRING SHOULD BE LOADED FROM .env'
    class Config:
        env_file = ".env"
        

@lru_cache
def app_settings():
    return AppSettings()
