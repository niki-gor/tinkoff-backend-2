from pydantic import SecretStr, BaseSettings


class AppSettings(BaseSettings):
    secret_key: SecretStr
    class Config:
        env_file = ".env"
        
    
    def __call__(self):
        return self


app_settings = AppSettings()