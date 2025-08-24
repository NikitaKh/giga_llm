from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent


class GigaChatModels:
    """Доступные модели GigaChat"""

    GIGACHAT_2_MAX = "GigaChat-2-Max"
    GIGACHAT_PRO = "GigaChat-Pro"
    GIGACHAT_PLUS = "GigaChat-Plus"


class BaseAppSettings(BaseSettings):
    """Базовые настройки приложения с конфигурацией окружения"""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_DIR / ".env"), env_file_encoding="utf-8", case_sensitive=False
    )


class Settings(BaseAppSettings):
    """Конфигурация приложения"""

    service_name: str = "AI_Chat"

    # GigaChat Credentials
    gigachat_api_key: str = ""
    gigachat_client_id: str = ""
    gigachat_scope: str = ""

    # Модели и параметры
    verify_ssl_certs: bool = False
    gigachat_model: str = GigaChatModels.GIGACHAT_2_MAX
    temperature: float = 0.2
    timeout: int = 1200
    system_prompt_template: str = ""


settings = Settings()
