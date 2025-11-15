# Arquitetura e-BrAIn.Tech v2.0

## Visão Geral

A plataforma e-BrAIn.Tech foi desenvolvida seguindo os princípios de **Clean Architecture** e **Design Patterns**, garantindo modularidade, escalabilidade e manutenibilidade.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │   Chat   │ │   Code   │ │Summarizer│ │   STT    │        │
│  │ Feature  │ │ Review   │ │ Feature  │ │ Feature  │        │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘        │
│       │            │            │            │              │
└───────┼────────────┼────────────┼────────────┼──────────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                      │
        ┌─────────────▼─────────────┐
        │     FEATURES LAYER        │
        │  (Business Logic)         │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │      CORE LAYER           │
        │  ┌──────────────────────┐ │
        │  │   LLMInterface       │ │
        │  │   (Abstract Base)    │ │
        │  └──────────┬───────────┘ │
        │             │             │
        │  ┌──────────▼───────────┐  │
        │  │ ContextManager       │  │
        │  │ HistoryManager       │  │
        │  │ ConfigLoader         │  │
        │  └──────────────────────┘  │
        └─────────────┬───────────────┘
                      │
        ┌─────────────▼─────────────┐
        │    PROVIDERS LAYER         │
        │  ┌──────────────────────┐  │
        │  │ ProviderFactory      │  │
        │  └──────────┬───────────┘  │
        │             │              │
        │  ┌──────────┴───────────┐  │
        │  │ OpenAIProvider       │  │
        │  │ AnthropicProvider    │  │
        │  │ MetaProvider         │  │
        │  │ OllamaProvider       │  │
        │  │ BedrockProvider      │  │
        │  │ GoogleProvider       │  │
        │  └──────────────────────┘  │
        └─────────────────────────────┘
                      │
        ┌─────────────▼─────────────┐
        │    EXTERNAL SERVICES       │
        │  OpenAI API                │
        │  Anthropic API             │
        │  AWS Bedrock               │
        │  Google Gemini API         │
        │  Ollama (Local)            │
        └─────────────────────────────┘
```

## Camadas da Arquitetura

### 1. Frontend Layer (Streamlit)

**Responsabilidade**: Interface do usuário

- **Componentes**:
  - `main_app.py`: Aplicação principal com abas
  - Layout responsivo e intuitivo
  - Gerenciamento de estado via `st.session_state`

**Características**:
- Abas modulares para cada funcionalidade
- Sidebar com configurações
- Visualização de histórico
- Estatísticas e métricas

### 2. Features Layer

**Responsabilidade**: Lógica de negócio específica

- **Features**:
  - `ChatFeature`: Conversação contextual
  - `CodeReviewFeature`: Revisão de código
  - `SummarizerFeature`: Sumarização
  - `STTFeature`: Transcrição de áudio
  - `ImageGenerationFeature`: Geração de imagens

**Padrão**: Cada feature herda de `BaseFeature` e implementa:
- `get_task_type()`: Define o tipo de tarefa
- `process()`: Processa a entrada e retorna resultado

### 3. Core Layer

**Responsabilidade**: Interfaces e abstrações centrais

#### LLMInterface (Abstract Base Class)

Define o contrato que todos os providers devem seguir:

```python
class LLMInterface(ABC):
    @abstractmethod
    def generate_text(...) -> LLMResponse
    @abstractmethod
    def generate_image(...) -> LLMResponse
    @abstractmethod
    def transcribe_audio(...) -> LLMResponse
    @abstractmethod
    def list_available_models() -> List[str]
```

#### ContextManager

Gerencia o contexto das conversas:
- Mantém histórico de mensagens por sessão
- Limita número de mensagens (configurável)
- Permite limpeza de contexto

#### HistoryManager

Gerencia histórico persistente:
- Armazena em SQLite
- Mantém últimas N interações
- Suporta consultas e estatísticas

#### ConfigLoader

Centraliza configurações:
- Carrega variáveis de ambiente
- Valida providers disponíveis
- Fornece configurações por provider

### 4. Providers Layer

**Responsabilidade**: Implementações de providers LLM

Cada provider implementa `LLMInterface`:

- **OpenAIProvider**: GPT-4o, DALL-E, Whisper
- **AnthropicProvider**: Claude 3.5 Sonnet
- **MetaProvider**: LLaMA via Ollama
- **OllamaProvider**: Modelos locais
- **BedrockProvider**: AWS Bedrock
- **GoogleProvider**: Gemini 1.5 Pro

**ProviderFactory**: Cria e gerencia instâncias de providers (Singleton pattern)

## Princípios de Design

### 1. Dependency Inversion

- Features dependem de abstrações (`LLMInterface`), não de implementações
- Facilita troca de providers sem modificar features

### 2. Single Responsibility

- Cada módulo tem uma responsabilidade única
- Features são independentes entre si

### 3. Open/Closed Principle

- Aberto para extensão (novos providers)
- Fechado para modificação (código existente)

### 4. Factory Pattern

- `ProviderFactory` centraliza criação de providers
- Evita acoplamento direto

### 5. Strategy Pattern

- Cada provider é uma estratégia diferente
- Intercambiáveis via interface comum

## Fluxo de Dados

### Exemplo: Chat Feature

```
1. Usuário digita mensagem no Frontend
   ↓
2. ChatFeature.process() é chamado
   ↓
3. ContextManager adiciona mensagem ao contexto
   ↓
4. ContextManager.get_context() retorna histórico
   ↓
5. Provider.generate_text() é chamado com contexto
   ↓
6. LLM retorna resposta
   ↓
7. ContextManager adiciona resposta ao contexto
   ↓
8. HistoryManager.save_interaction() persiste
   ↓
9. Frontend exibe resposta ao usuário
```

## Extensibilidade

### Adicionar Novo Provider

1. Criar `app/providers/novo_provider.py`
2. Herdar de `LLMInterface`
3. Implementar métodos abstratos
4. Registrar no `ProviderFactory`

### Adicionar Nova Feature

1. Criar `app/features/nova_feature.py`
2. Herdar de `BaseFeature`
3. Implementar `get_task_type()` e `process()`
4. Adicionar aba no `main_app.py`

## Segurança

- ✅ Credenciais via variáveis de ambiente
- ✅ Sem hardcode de secrets
- ✅ Validação de configuração
- ✅ Tratamento de erros robusto

## Performance

- ✅ Contexto limitado (evita tokens excessivos)
- ✅ Histórico com limite configurável
- ✅ Providers reutilizados (singleton)
- ✅ SQLite para histórico local

## Testabilidade

- ✅ Interfaces facilitam mocks
- ✅ Features isoladas e testáveis
- ✅ Providers independentes
- ✅ Configuração injetável

## Manutenibilidade

- ✅ Código modular e organizado
- ✅ Documentação inline
- ✅ Separação clara de responsabilidades
- ✅ Fácil localização de bugs

---

**Versão**: 2.0  
**Última atualização**: 2024-10-22

