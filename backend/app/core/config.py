from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    backend_env: str = "development"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    backend_log_level: str = "info"

    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()