"""LLM service for integrating various AI capabilities."""
from typing import List, Dict, Optional, AsyncGenerator
from openai import AsyncOpenAI
from config import settings
import json


class LLMService:
    """Service for handling LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM service with OpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = "gpt-4-turbo-preview"
    
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None] | Dict:
        """
        Send a chat request to the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            AsyncGenerator for streaming or Dict for non-streaming responses
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        if stream:
            async def generate():
                async for chunk in await self.client.chat.completions.create(**kwargs):
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return generate()
        else:
            response = await self.client.chat.completions.create(**kwargs)
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
    
    async def analyze_document(self, document_text: str, query: str) -> Dict:
        """
        Analyze a document and answer questions about it.
        
        Args:
            document_text: The text content of the document
            query: The question or analysis request
            
        Returns:
            Dict with analysis results
        """
        messages = [
            {
                "role": "system",
                "content": "Você é um assistente especializado em análise de documentos. Analise o documento fornecido e responda às perguntas de forma clara e objetiva."
            },
            {
                "role": "user",
                "content": f"Documento:\n{document_text}\n\nPergunta: {query}"
            }
        ]
        
        return await self.chat(messages)
    
    async def generate_code(self, description: str, language: str = "python") -> Dict:
        """
        Generate code based on a description.
        
        Args:
            description: Description of what the code should do
            language: Programming language for the code
            
        Returns:
            Dict with generated code
        """
        messages = [
            {
                "role": "system",
                "content": f"Você é um assistente especializado em programação. Gere código {language} limpo, bem documentado e seguindo as melhores práticas."
            },
            {
                "role": "user",
                "content": description
            }
        ]
        
        return await self.chat(messages)
    
    async def review_code(self, code: str, language: str = "python") -> Dict:
        """
        Review code and provide suggestions for improvement.
        
        Args:
            code: The code to review
            language: Programming language of the code
            
        Returns:
            Dict with review results
        """
        messages = [
            {
                "role": "system",
                "content": "Você é um revisor de código experiente. Analise o código fornecido e forneça feedback sobre qualidade, segurança, performance e melhores práticas."
            },
            {
                "role": "user",
                "content": f"Linguagem: {language}\n\nCódigo:\n```{language}\n{code}\n```"
            }
        ]
        
        return await self.chat(messages)
    
    async def analyze_data(self, data: str, query: str) -> Dict:
        """
        Analyze data and provide insights.
        
        Args:
            data: The data to analyze (CSV, JSON, or text format)
            query: The analysis request or question
            
        Returns:
            Dict with analysis results
        """
        messages = [
            {
                "role": "system",
                "content": "Você é um analista de dados especializado. Analise os dados fornecidos e forneça insights relevantes, estatísticas e visualizações quando apropriado."
            },
            {
                "role": "user",
                "content": f"Dados:\n{data}\n\nAnálise solicitada: {query}"
            }
        ]
        
        return await self.chat(messages)


# Global LLM service instance
llm_service = LLMService()
