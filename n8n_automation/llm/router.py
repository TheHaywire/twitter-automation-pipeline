from typing import List, Any
from .gemini import GeminiLLM

class LLMRouter:
    """
    Routes requests to the best LLM provider, with fallback and load balancing.
    Currently supports only Gemini, but can be extended.
    """
    def __init__(self, providers: List[Any] = None):
        if providers is None:
            providers = [GeminiLLM()]
        self.providers = providers

    def generate(self, prompt: str, **kwargs) -> str:
        for provider in self.providers:
            try:
                return provider.generate(prompt, **kwargs)
            except Exception as e:
                continue
        raise RuntimeError("All LLM providers failed.")
