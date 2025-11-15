"""
Factory para criar instâncias de providers
"""
from typing import Dict, Optional, List
from providers import (
    OpenAIProvider,
    AnthropicProvider,
    BedrockProvider,
    OllamaProvider,
    BaseProvider
)
import config

class ProviderFactory:
    """Factory para gerenciar providers"""
    
    _providers: Dict[str, BaseProvider] = {}
    
    @classmethod
    def get_provider(cls, provider_name: str) -> Optional[BaseProvider]:
        """
        Retorna uma instância do provider solicitado
        Cria uma nova instância se não existir
        """
        provider_name_lower = provider_name.lower()
        
        if provider_name_lower not in cls._providers:
            if provider_name_lower == "openai":
                cls._providers[provider_name_lower] = OpenAIProvider()
            elif provider_name_lower == "anthropic":
                cls._providers[provider_name_lower] = AnthropicProvider()
            elif provider_name_lower == "aws_bedrock" or provider_name_lower == "bedrock":
                cls._providers[provider_name_lower] = BedrockProvider()
            elif provider_name_lower == "ollama":
                cls._providers[provider_name_lower] = OllamaProvider()
            else:
                return None
        
        return cls._providers.get(provider_name_lower)
    
    @classmethod
    def get_available_providers(cls) -> Dict[str, bool]:
        """Retorna um dicionário com os providers disponíveis"""
        providers = {
            "OpenAI": OpenAIProvider(),
            "Anthropic": AnthropicProvider(),
            "AWS Bedrock": BedrockProvider(),
            "Ollama": OllamaProvider(),
        }
        
        return {
            name: provider.is_available()
            for name, provider in providers.items()
        }
    
    @classmethod
    def get_provider_list(cls) -> List[str]:
        """Retorna lista de nomes de providers disponíveis"""
        available = cls.get_available_providers()
        return [name for name, is_avail in available.items() if is_avail]

