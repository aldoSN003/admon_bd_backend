from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # /home/.../admon_bd_backend
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    # Database Configuration
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Application Configuration
    APP_NAME: str = "GuardianFace API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),  # <---- load .env ABSOLUTELY CORRECT
        extra="ignore",
        case_sensitive=True,
    )

    @property
    def database_url(self) -> str:
        from urllib.parse import quote_plus
        password = quote_plus(self.DB_PASSWORD)
        return (
            f"mysql+pymysql://{self.DB_USER}:{password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
