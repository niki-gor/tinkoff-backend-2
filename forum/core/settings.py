from pydantic import BaseSettings, PostgresDsn, SecretStr


class AppSettings(BaseSettings):
    secret_key: SecretStr
    dsn: PostgresDsn
    min_connection_count: int
    max_connection_count: int
