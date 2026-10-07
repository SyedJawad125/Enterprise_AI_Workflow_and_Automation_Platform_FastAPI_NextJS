from app.core.config import LLM_PROVIDER
from app.providers.base import LLMProvider
from app.providers.mock_provider import MockProvider


def get_provider() -> LLMProvider:
    if LLM_PROVIDER == "openai":
        from app.providers.openai_provider import OpenAIProvider
        return OpenAIProvider()
    if LLM_PROVIDER == "groq":
        from app.providers.groq_provider import GroqProvider
        return GroqProvider()
    if LLM_PROVIDER == "gemini":
        from app.providers.gemini_provider import GeminiProvider
        return GeminiProvider()
    return MockProvider()
