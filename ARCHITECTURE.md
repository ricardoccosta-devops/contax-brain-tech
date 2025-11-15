# Arquitetura do e-BrAIn.Tech

Este documento descreve a arquitetura modular do portal e-BrAIn.Tech e como adicionar novos providers ou funcionalidades.

## 🏗️ Visão Geral da Arquitetura

A aplicação foi projetada com uma arquitetura modular que permite:
- Adicionar novos providers sem modificar código existente
- Manter cada módulo independente
- Facilitar testes e manutenção
- Escalar facilmente

```
┌─────────────────────────────────────────┐
│         app.py (Streamlit UI)          │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────┐
│   Factory   │  │  History Manager│
│  (Providers)│  │   (Storage)     │
└──────┬──────┘  └─────────────────┘
       │
┌──────▼──────────────────────────┐
│      BaseProvider (ABC)          │
│  ┌──────────────────────────┐   │
│  │  OpenAIProvider          │   │
│  │  AnthropicProvider       │   │
│  │  BedrockProvider         │   │
│  │  OllamaProvider          │   │
│  │  [NovoProvider]          │   │
│  └──────────────────────────┘   │
└──────────────────────────────────┘
```

## 📦 Estrutura de Módulos

### 1. `config.py` - Configuração Centralizada

**Responsabilidade**: Carregar e gerenciar todas as variáveis de ambiente.

**Como usar**:
```python
import config

# Acessa variáveis
api_key = config.Config.OPENAI_API_KEY

# Valida providers
status = config.Config.validate()
```

**Adicionar nova variável**:
1. Adicione a variável na classe `Config`
2. Use `os.getenv()` para carregar do ambiente
3. Forneça valor padrão se necessário

### 2. `providers/base.py` - Interface Base

**Responsabilidade**: Define a interface que todos os providers devem implementar.

**Componentes principais**:
- `BaseProvider`: Classe abstrata base
- `ModelType`: Enum com tipos de modelos
- `Message`: Classe para representar mensagens

**Métodos obrigatórios**:
- `is_available()`: Verifica se o provider está configurado
- `chat_completion()`: Gera respostas
- `list_models()`: Lista modelos disponíveis

### 3. `providers/*_provider.py` - Implementações

Cada provider implementa a interface `BaseProvider`.

**Estrutura padrão**:
```python
from providers.base import BaseProvider, Message, ModelType

class NovoProvider(BaseProvider):
    def __init__(self):
        super().__init__("Nome do Provider")
        # Inicialização
    
    def is_available(self) -> bool:
        # Verifica disponibilidade
        pass
    
    def chat_completion(self, messages, model_type, **kwargs):
        # Implementa lógica de geração
        pass
    
    def list_models(self):
        # Retorna lista de modelos
        pass
```

### 4. `utils/provider_factory.py` - Factory Pattern

**Responsabilidade**: Criar e gerenciar instâncias de providers.

**Como adicionar novo provider**:
1. Crie o arquivo do provider em `providers/`
2. Adicione no `ProviderFactory.get_provider()`:
```python
elif provider_name_lower == "novo_provider":
    cls._providers[provider_name_lower] = NovoProvider()
```
3. Adicione em `get_available_providers()`:
```python
providers = {
    ...
    "Novo Provider": NovoProvider(),
}
```

### 5. `utils/history.py` - Gerenciamento de Histórico

**Responsabilidade**: Armazenar e recuperar histórico de interações.

**Funcionalidades**:
- Salvar interações em JSON
- Limitar a 90 interações (configurável)
- Recuperar interações específicas
- Limpar histórico

### 6. `app.py` - Interface Streamlit

**Responsabilidade**: Interface do usuário e orquestração.

**Componentes**:
- Sidebar: Configurações e histórico
- Área principal: Chat interface
- Gerenciamento de estado via `st.session_state`

## 🔌 Adicionando um Novo Provider

### Passo 1: Criar o Provider

Crie `providers/novo_provider.py`:

```python
"""
Provider para [Nome do Serviço]
"""
from typing import List, Dict, Any
import config
from providers.base import BaseProvider, Message, ModelType

class NovoProvider(BaseProvider):
    """Provider para [Nome]"""
    
    def __init__(self):
        super().__init__("Nome do Provider")
        # Inicialize cliente/API aqui
        self.client = None
        if config.Config.NOVA_API_KEY:
            self.client = ClienteAPI(api_key=config.Config.NOVA_API_KEY)
    
    def is_available(self) -> bool:
        """Verifica se está configurado"""
        return self.client is not None
    
    def chat_completion(
        self,
        messages: List[Message],
        model_type: ModelType,
        **kwargs
    ) -> Dict[str, Any]:
        """Gera resposta"""
        if not self.is_available():
            raise ValueError("Provider não configurado")
        
        # Implemente a lógica aqui
        # Use self.get_system_prompt(model_type) para prompt do sistema
        
        return {
            "content": "Resposta do provider"
        }
    
    def list_models(self) -> List[str]:
        """Lista modelos disponíveis"""
        return ["modelo1", "modelo2"]
```

### Passo 2: Adicionar Variáveis de Ambiente

Em `config.py`:

```python
class Config:
    # ... existentes ...
    
    # Novo Provider
    NOVA_API_KEY: Optional[str] = os.getenv("NOVA_API_KEY")
    NOVA_MODEL: str = os.getenv("NOVA_MODEL", "modelo-padrao")
```

### Passo 3: Registrar no Factory

Em `utils/provider_factory.py`:

```python
from providers.novo_provider import NovoProvider

class ProviderFactory:
    @classmethod
    def get_provider(cls, provider_name: str):
        # ...
        elif provider_name_lower == "novo_provider":
            cls._providers[provider_name_lower] = NovoProvider()
        # ...
    
    @classmethod
    def get_available_providers(cls):
        providers = {
            # ...
            "Novo Provider": NovoProvider(),
        }
        # ...
```

### Passo 4: Atualizar Imports

Em `providers/__init__.py`:

```python
from providers.novo_provider import NovoProvider

__all__ = [
    # ...
    "NovoProvider",
]
```

## 🧪 Testando um Provider

Crie um script de teste:

```python
from providers.novo_provider import NovoProvider
from providers.base import Message, ModelType

provider = NovoProvider()

# Testa disponibilidade
print(f"Disponível: {provider.is_available()}")

# Testa chat
messages = [
    Message(role="user", content="Olá!")
]
response = provider.chat_completion(
    messages=messages,
    model_type=ModelType.TEXT_COMPLETION
)
print(response)
```

## 🔄 Princípios de Design

### 1. Separação de Responsabilidades

Cada módulo tem uma responsabilidade única:
- `config.py`: Configuração
- `providers/`: Lógica de providers
- `utils/`: Utilitários
- `app.py`: Interface

### 2. Inversão de Dependência

Providers dependem da abstração (`BaseProvider`), não de implementações específicas.

### 3. Factory Pattern

Centraliza criação de objetos, facilitando adição de novos providers.

### 4. Singleton (parcial)

Providers são criados uma vez e reutilizados via Factory.

## 📝 Boas Práticas

### 1. Tratamento de Erros

Sempre trate erros adequadamente:

```python
try:
    response = self.client.call()
except SpecificError as e:
    raise ValueError(f"Erro específico: {str(e)}")
except Exception as e:
    raise ValueError(f"Erro inesperado: {str(e)}")
```

### 2. Validação

Valide inputs antes de processar:

```python
if not messages:
    raise ValueError("Lista de mensagens vazia")
```

### 3. Documentação

Documente todos os métodos e classes:

```python
def metodo(self, param: str) -> Dict:
    """
    Descrição do método
    
    Args:
        param: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
        
    Raises:
        ValueError: Quando algo dá errado
    """
    pass
```

### 4. Type Hints

Use type hints sempre:

```python
def funcao(self, param: str) -> Dict[str, Any]:
    pass
```

## 🚀 Extensibilidade

### Adicionar Novo Tipo de Modelo

1. Adicione ao enum `ModelType` em `providers/base.py`:
```python
class ModelType(Enum):
    # ... existentes ...
    NOVO_TIPO = "novo-tipo"
```

2. Adicione prompt do sistema em `BaseProvider.__init__()`:
```python
self.system_prompts = {
    # ... existentes ...
    ModelType.NOVO_TIPO: "Prompt para novo tipo",
}
```

3. Atualize `app.py` para incluir na UI

### Adicionar Nova Funcionalidade

1. Identifique onde a funcionalidade se encaixa
2. Crie módulo separado se necessário
3. Mantenha baixo acoplamento
4. Documente extensivamente

## 🔍 Debugging

### Logs

Adicione logs quando necessário:

```python
import logging

logger = logging.getLogger(__name__)

def metodo(self):
    logger.debug("Mensagem de debug")
    logger.error("Erro ocorreu")
```

### Testes Locais

Teste providers isoladamente antes de integrar:

```python
# test_provider.py
from providers.novo_provider import NovoProvider

provider = NovoProvider()
# Testes aqui
```

## 📚 Recursos Adicionais

- [Documentação Python ABC](https://docs.python.org/3/library/abc.html)
- [Design Patterns em Python](https://refactoring.guru/design-patterns/python)
- [Streamlit Best Practices](https://docs.streamlit.io/)

