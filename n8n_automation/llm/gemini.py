import os
import google.generativeai as genai
from typing import Optional

class GeminiLLM:
    """
    Wrapper for the Gemini LLM (Google Generative AI API).
    """
    def __init__(self, api_key: Optional[str] = None, model: str = 'gemini-2.5-flash'):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model_name = model
        if not self.api_key:
            raise ValueError('GEMINI_API_KEY not set in environment or provided.')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from the Gemini LLM.
        Args:
            prompt: The prompt to send to the LLM.
        Returns:
            The generated text.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini LLM error: {e}")
