"""
Provider para Anthropic (Claude)
"""
from typing import List, Dict, Any
from anthropic import Anthropic
import config
from providers.base import BaseProvider, Message, ModelType

class AnthropicProvider(BaseProvider):
    """Provider para Anthropic Claude"""
    
    def __init__(self):
        super().__init__("Anthropic")
        self.client = None
        if config.Config.ANTHROPIC_API_KEY:
            self.client = Anthropic(api_key=config.Config.ANTHROPIC_API_KEY)
    
    def is_available(self) -> bool:
        """Verifica se Anthropic está configurado"""
        return self.client is not None
    
    def chat_completion(
        self,
        messages: List[Message],
        model_type: ModelType,
        **kwargs
    ) -> Dict[str, Any]:
        """Gera resposta usando Claude"""
        if not self.is_available():
            raise ValueError("Anthropic não está configurado")
        
        # Claude não suporta geração de imagens
        if model_type == ModelType.IMAGE_CREATION:
            return {
                "content": "Geração de imagens não é suportada pelo Claude. Por favor, use OpenAI para esta funcionalidade."
            }
        
        system_prompt = self.get_system_prompt(model_type)
        
        # Converte mensagens para formato Anthropic
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Ajusta max_tokens baseado no tipo de modelo
        max_tokens = 2000
        if model_type == ModelType.SUMMARIZATION:
            max_tokens = 1000
        
        response = self.client.messages.create(
            model=config.Config.ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=anthropic_messages
        )
        
        # Claude retorna uma lista de blocos de conteúdo
        content = ""
        for block in response.content:
            if block.type == "text":
                content += block.text
        
        return {
            "content": content
        }
    
    def list_models(self) -> List[str]:
        """Lista modelos Anthropic disponíveis"""
        return [
            "claude-3-5-sonnet-20241022",  # Modelo mais recente: Claude 3.5 Sonnet (outubro 2024)
            "claude-3-5-haiku-20241022",  # Claude 3.5 Haiku (outubro 2024)
            "claude-3-5-sonnet-20240620",  # Claude 3.5 Sonnet (junho 2024)
            "claude-3-opus-20240229",      # Claude 3 Opus
            "claude-3-sonnet-20240229",    # Claude 3 Sonnet
            "claude-3-haiku-20240307"      # Claude 3 Haiku
        ]

