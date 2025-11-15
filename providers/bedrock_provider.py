"""
Provider para AWS Bedrock
"""
from typing import List, Dict, Any
import boto3
import json
import config
from providers.base import BaseProvider, Message, ModelType

class BedrockProvider(BaseProvider):
    """Provider para AWS Bedrock"""
    
    def __init__(self):
        super().__init__("AWS Bedrock")
        self.client = None
        if config.Config.AWS_ACCESS_KEY_ID and config.Config.AWS_SECRET_ACCESS_KEY:
            self.client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=config.Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.Config.AWS_SECRET_ACCESS_KEY,
                region_name=config.Config.AWS_REGION
            )
    
    def is_available(self) -> bool:
        """Verifica se AWS Bedrock está configurado"""
        return self.client is not None
    
    def chat_completion(
        self,
        messages: List[Message],
        model_type: ModelType,
        **kwargs
    ) -> Dict[str, Any]:
        """Gera resposta usando AWS Bedrock"""
        if not self.is_available():
            raise ValueError("AWS Bedrock não está configurado")
        
        # Bedrock não suporta geração de imagens via API padrão
        if model_type == ModelType.IMAGE_CREATION:
            return {
                "content": "Geração de imagens não é suportada pelo AWS Bedrock. Por favor, use OpenAI para esta funcionalidade."
            }
        
        system_prompt = self.get_system_prompt(model_type)
        
        # Converte mensagens para formato Bedrock (Anthropic Claude)
        # Bedrock usa formato similar ao Anthropic
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": [{"type": "text", "text": msg.content}]
            })
        
        # Ajusta max_tokens baseado no tipo de modelo
        max_tokens = 2000
        if model_type == ModelType.SUMMARIZATION:
            max_tokens = 1000
        
        # Prepara o body para Bedrock
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": formatted_messages
        })
        
        try:
            response = self.client.invoke_model(
                modelId=config.Config.AWS_BEDROCK_MODEL,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extrai o conteúdo da resposta
            content = ""
            for block in response_body.get('content', []):
                if block.get('type') == 'text':
                    content += block.get('text', '')
            
            return {
                "content": content
            }
        except Exception as e:
            raise ValueError(f"Erro ao chamar AWS Bedrock: {str(e)}")
    
    def list_models(self) -> List[str]:
        """Lista modelos AWS Bedrock disponíveis"""
        return [
            "anthropic.claude-3-5-sonnet-20240620-v2:0",  # Modelo mais recente: Claude 3.5 Sonnet
            "anthropic.claude-3-5-haiku-20241022-v1:0",   # Claude 3.5 Haiku (outubro 2024)
            "anthropic.claude-3-opus-20240229-v1:0",     # Claude 3 Opus
            "anthropic.claude-3-sonnet-20240229-v1:0",   # Claude 3 Sonnet
            "anthropic.claude-3-haiku-20240307-v1:0",    # Claude 3 Haiku
            "amazon.titan-text-premier-v1:0",            # Amazon Titan Premier (mais recente)
            "amazon.titan-text-express-v1",              # Amazon Titan Express
            "amazon.titan-text-lite-v1"                  # Amazon Titan Lite
        ]

