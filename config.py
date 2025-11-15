"""
Configuração centralizada do portal e-BrAIn.Tech
Todas as variáveis de ambiente são carregadas aqui
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações do portal"""
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")  # Modelo mais recente: GPT-4o
    
    # Anthropic (Claude)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")  # Modelo mais recente: Claude 3.5 Sonnet
    
    # AWS Bedrock
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_BEDROCK_MODEL: str = os.getenv("AWS_BEDROCK_MODEL", "anthropic.claude-3-5-sonnet-20240620-v1:0")  # Modelo mais recente: Claude 3.5 Sonnet
    
    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")  # Modelo mais recente: Llama 3.1
    
    # Configurações gerais
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "90"))
    HISTORY_FILE: str = os.getenv("HISTORY_FILE", "history.json")
    
    @classmethod
    def validate(cls) -> dict:
        """
        Valida quais providers estão configurados
        Retorna um dicionário com o status de cada provider
        """
        return {
            "openai": cls.OPENAI_API_KEY is not None,
            "anthropic": cls.ANTHROPIC_API_KEY is not None,
            "aws_bedrock": cls.AWS_ACCESS_KEY_ID is not None and cls.AWS_SECRET_ACCESS_KEY is not None,
            "ollama": True,  # Ollama pode estar rodando localmente sem credenciais
        }

