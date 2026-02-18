"""
OpenRouter AI Service
Handles AI model selection and content generation
"""
import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class OpenRouterAI:
    """OpenRouter AI API Integration"""
    
    # Available models (updated with correct OpenRouter IDs)
    MODELS = {
        "GPT-4 Turbo": "openai/gpt-4-turbo-preview",
        "GPT-4": "openai/gpt-4",
        "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
        "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
        "Claude 3 Opus": "anthropic/claude-3-opus-20240229",
        "Claude 3 Haiku": "anthropic/claude-3-haiku-20240307",
        "Gemini Pro": "google/gemini-pro-1.5",
        "Llama 3.1 70B": "meta-llama/llama-3.1-70b-instruct",
        "Mixtral 8x7B": "mistralai/mixtral-8x7b-instruct",
    }
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.site_url = os.getenv('OPENROUTER_SITE_URL', 'https://ai-content-engine.app')
        self.site_name = os.getenv('OPENROUTER_SITE_NAME', 'AI Content Engine')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    def generate(self, prompt: str, model: str = "openai/gpt-3.5-turbo", max_tokens: int = 2000) -> Optional[str]:
        """
        Generate content using OpenRouter AI
        
        Args:
            prompt: The prompt to send to the AI
            model: Model identifier (use MODELS dict)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text or None if error
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": self.site_url,
                "X-Title": self.site_name,
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(data),
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Generation error: {e}")
            return None
    
    @classmethod
    def get_model_list(cls) -> Dict[str, str]:
        """Get list of available models"""
        return cls.MODELS
    
    @classmethod
    def get_model_names(cls) -> list:
        """Get list of model display names"""
        return list(cls.MODELS.keys())
