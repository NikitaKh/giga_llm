import logging
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from app.settings import settings

logger = logging.getLogger(__name__)


def create_gigachat_with_params(
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None,
        verify_ssl_certs: Optional[bool] = None,
) -> GigaChat:
    """Создает GigaChat LLM с переданными параметрами."""
    return _create_gigachat_instance(
        model=model or settings.gigachat_model,
        temperature=temperature if temperature is not None else settings.temperature,
        timeout=timeout or settings.timeout,
        verify_ssl_certs=verify_ssl_certs if verify_ssl_certs is not None else settings.verify_ssl_certs,
    )


def _validate_gigachat_params(
        model: str,
        temperature: float,
        timeout: int,
) -> None:
    """Валидирует параметры GigaChat."""
    if not isinstance(temperature, (int, float)) or not 0.0 <= temperature <= 2.0:
        raise ValueError(f"Температура должна быть в диапазоне [0.0, 2.0], получено: {temperature}")

    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError(f"Таймаут должен быть положительным числом, получено: {timeout}")

    if not isinstance(model, str) or not model.strip():
        raise ValueError(f"Модель должна быть непустой строкой, получено: {model}")


def _create_gigachat_instance(
        model: str,
        temperature: float,
        timeout: int,
        verify_ssl_certs: bool,
) -> GigaChat:
    """Создает экземпляр GigaChat с валидацией параметров."""
    _validate_gigachat_params(model, temperature, timeout)

    if not settings.gigachat_api_key or not settings.gigachat_scope:
        raise ValueError("Отсутствуют обязательные параметры: GIGACHAT_API_KEY или GIGACHAT_SCOPE")

    try:
        llm = GigaChat(
            scope=settings.gigachat_scope,
            credentials=settings.gigachat_api_key,
            model=model,
            verify_ssl_certs=verify_ssl_certs,
            timeout=timeout,
            temperature=temperature,
        )
        logger.info(f"GigaChat LLM создан: модель={model}, температура={temperature}")
        return llm

    except Exception as e:
        error_msg = f"Ошибка создания GigaChat LLM: {e}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e


def invoke_gigachat_with_system_prompt(
        llm: GigaChat,
        user_message: str,
        system_prompt: str
) -> str:
    """
    Вызов GigaChat с системным промптом.

    Args:
        llm: Экземпляр GigaChat
        user_message: Сообщение пользователя
        system_prompt: Системный промпт для контекста

    Returns:
        str: Ответ от модели

    Raises:
        ValueError: При некорректных входных данных
        RuntimeError: При ошибке вызова модели
    """
    if not user_message or not user_message.strip():
        raise ValueError("Сообщение пользователя не может быть пустым")

    if not system_prompt or not system_prompt.strip():
        raise ValueError("Системный промпт не может быть пустым")

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]

        response = llm.invoke(messages)
        result = response.content if hasattr(response, 'content') else str(response)

        if not result:
            raise RuntimeError("Получен пустой ответ от модели")

        logger.debug(f"GigaChat ответ с системным промптом получен, длина: {len(result)} символов")
        return result.strip()

    except Exception as e:
        error_msg = f"Ошибка вызова GigaChat с системным промптом: {e}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e


def generate_response_with_system_prompt(
        user_message: str,
        system_prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
) -> str:
    """
    Генерирует ответ с системным промптом.

    Args:
        user_message: Сообщение пользователя
        system_prompt: Системный промпт
        model: Модель GigaChat (опционально)
        temperature: Температура генерации (опционально)

    Returns:
        str: Ответ от модели

    Raises:
        ValueError: При некорректных входных данных
        RuntimeError: При ошибке генерации
    """
    if not user_message or not user_message.strip():
        raise ValueError("Сообщение пользователя не может быть пустым")

    if not system_prompt or not system_prompt.strip():
        raise ValueError("Системный промпт не может быть пустым")

    try:
        llm = create_gigachat_with_params(
            model=model,
            temperature=temperature
        )

        return invoke_gigachat_with_system_prompt(llm, user_message, system_prompt)

    except Exception as e:
        error_msg = f"Ошибка генерации ответа с системным промптом: {e}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e
