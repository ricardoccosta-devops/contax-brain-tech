"""
Provider para OpenAI (GPT-4o, GPT-4 Turbo, DALL-E, Whisper)
"""
from typing import List, Dict, Any
from openai import OpenAI
import config
from providers.base import BaseProvider, Message, ModelType

class OpenAIProvider(BaseProvider):
    """Provider para OpenAI"""
    
    def __init__(self):
        super().__init__("OpenAI")
        self.client = None
        if config.Config.OPENAI_API_KEY:
            self.client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    
    def is_available(self) -> bool:
        """Verifica se OpenAI está configurado"""
        return self.client is not None
    
    def chat_completion(
        self,
        messages: List[Message],
        model_type: ModelType,
        **kwargs
    ) -> Dict[str, Any]:
        """Gera resposta usando OpenAI"""
        if not self.is_available():
            raise ValueError("OpenAI não está configurado")
        
        # Geração de imagens
        if model_type == ModelType.IMAGE_CREATION:
            last_message = messages[-1] if messages else None
            if not last_message:
                raise ValueError("Prompt necessário para geração de imagem")
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=last_message.content,
                n=1,
                size="1024x1024"
            )
            
            return {
                "content": f"Imagem gerada baseada em: \"{last_message.content}\"",
                "image_url": response.data[0].url
            }
        
        # Chat completion
        system_prompt = self.get_system_prompt(model_type)
        
        # Converte mensagens para formato OpenAI
        openai_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Ajusta max_tokens baseado no tipo de modelo
        max_tokens = 2000
        if model_type == ModelType.SUMMARIZATION:
            max_tokens = 1000
        
        response = self.client.chat.completions.create(
            model=config.Config.OPENAI_MODEL,
            messages=openai_messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return {
            "content": response.choices[0].message.content
        }
    
    def list_models(self) -> List[str]:
        """Lista modelos OpenAI disponíveis"""
        return [
            "gpt-4o",              # Modelo mais recente e avançado (2024)
            "gpt-4o-mini",         # Versão mais rápida e econômica do GPT-4o
            "gpt-4-turbo",         # GPT-4 Turbo
            "gpt-4",               # GPT-4 padrão
            "gpt-3.5-turbo",       # GPT-3.5 Turbo (mais econômico)
            "dall-e-3",            # Geração de imagens
            "whisper-1"            # Speech-to-text
        ]

