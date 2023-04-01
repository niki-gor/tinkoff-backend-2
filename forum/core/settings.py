from pydantic import PostgresDsn, SecretStr, BaseSettings


class AppSettings(BaseSettings):
    secret_key: SecretStr
    dsn: PostgresDsn
    min_connection_count: int = 10
    max_connection_count: int = 20
