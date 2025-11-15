"""
Provider para Ollama (LLMs locais)
"""
from typing import List, Dict, Any
import requests
import config
from providers.base import BaseProvider, Message, ModelType

class OllamaProvider(BaseProvider):
    """Provider para Ollama"""
    
    def __init__(self):
        super().__init__("Ollama")
        self.base_url = config.Config.OLLAMA_BASE_URL
    
    def is_available(self) -> bool:
        """Verifica se Ollama está disponível"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def chat_completion(
        self,
        messages: List[Message],
        model_type: ModelType,
        **kwargs
    ) -> Dict[str, Any]:
        """Gera resposta usando Ollama"""
        if not self.is_available():
            raise ValueError("Ollama não está disponível. Certifique-se de que o serviço está rodando.")
        
        # Ollama não suporta geração de imagens
        if model_type == ModelType.IMAGE_CREATION:
            return {
                "content": "Geração de imagens não é suportada pelo Ollama. Por favor, use OpenAI para esta funcionalidade."
            }
        
        system_prompt = self.get_system_prompt(model_type)
        
        # Converte mensagens para formato Ollama
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Prepara o payload para Ollama
        payload = {
            "model": config.Config.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                *formatted_messages
            ],
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "content": result.get("message", {}).get("content", "")
            }
        except Exception as e:
            raise ValueError(f"Erro ao chamar Ollama: {str(e)}")
    
    def list_models(self) -> List[str]:
        """Lista modelos Ollama disponíveis"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model.get("name", "") for model in models]
        except:
            pass
        # Modelos mais recentes e populares do Ollama
        return [
            "llama3.1",           # Llama 3.1 (mais recente)
            "llama3",             # Llama 3
            "llama2",             # Llama 2
            "mistral",            # Mistral
            "mixtral",            # Mixtral (mais recente)
            "codellama",          # Code Llama
            "phi3",               # Phi-3 (mais recente)
            "phi",                # Phi
            "gemma2",             # Gemma 2 (mais recente)
            "gemma",              # Gemma
            "qwen2.5",            # Qwen 2.5 (mais recente)
            "neural-chat"         # Neural Chat
        ]

