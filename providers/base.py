"""
Classe base abstrata para todos os providers de LLM
Cada provider deve implementar esta interface
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from enum import Enum

class ModelType(Enum):
    """Tipos de modelos disponíveis"""
    CODE_REVIEW = "code-review"
    TEXT_COMPLETION = "text-completion"
    SUMMARIZATION = "summarization"
    SPEECH_TO_TEXT = "speech-to-text"
    IMAGE_CREATION = "image-creation"

class Message:
    """Representa uma mensagem na conversa"""
    def __init__(self, role: str, content: str):
        self.role = role  # 'user' ou 'assistant'
        self.content = content

class BaseProvider(ABC):
    """Classe base para todos os providers de LLM"""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.system_prompts = {
            ModelType.CODE_REVIEW: "You are an expert code reviewer. Provide detailed feedback, suggestions, and improvements for the code provided. Focus on best practices, performance, security, and maintainability.",
            ModelType.TEXT_COMPLETION: "You are a helpful AI assistant that completes text in a coherent and contextually appropriate manner.",
            ModelType.SUMMARIZATION: "You are an expert at summarizing content. Provide concise, accurate summaries that capture the key points and main ideas.",
            ModelType.SPEECH_TO_TEXT: "You are a speech-to-text transcription expert.",
            ModelType.IMAGE_CREATION: "You are an image generation assistant.",
        }
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provider está disponível e configurado"""
        pass
    
    @abstractmethod
    def chat_completion(
        self,
        messages: List[Message],
        model_type: ModelType,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Gera uma resposta baseada nas mensagens fornecidas
        
        Args:
            messages: Lista de mensagens da conversa
            model_type: Tipo de modelo a ser usado
            **kwargs: Parâmetros adicionais específicos do provider
            
        Returns:
            Dict com 'content' (texto da resposta) e opcionalmente 'image_url' (para geração de imagens)
        """
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """Lista os modelos disponíveis para este provider"""
        pass
    
    def get_system_prompt(self, model_type: ModelType) -> str:
        """Retorna o prompt do sistema para o tipo de modelo"""
        return self.system_prompts.get(model_type, "You are a helpful AI assistant.")

