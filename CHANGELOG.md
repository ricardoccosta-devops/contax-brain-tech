# Changelog - e-BrAIn.Tech

## [1.1.0] - 2024-10-22

### 🚀 Atualizações de Modelos

#### OpenAI
- ✅ **Atualizado modelo padrão**: `gpt-4` → `gpt-4o` (modelo mais recente e avançado)
- ✅ **Adicionado**: `gpt-4o-mini` (versão mais rápida e econômica)
- ✅ **Modelos disponíveis atualizados**:
  - `gpt-4o` - Modelo mais recente (2024)
  - `gpt-4o-mini` - Versão otimizada
  - `gpt-4-turbo` - GPT-4 Turbo
  - `gpt-4` - GPT-4 padrão
  - `gpt-3.5-turbo` - GPT-3.5 Turbo

#### Anthropic (Claude)
- ✅ **Atualizado modelo padrão**: `claude-3-opus-20240229` → `claude-3-5-sonnet-20241022`
- ✅ **Adicionado**: Claude 3.5 Sonnet (outubro 2024) - modelo mais recente
- ✅ **Adicionado**: Claude 3.5 Haiku (outubro 2024)
- ✅ **Modelos disponíveis atualizados**:
  - `claude-3-5-sonnet-20241022` - Mais recente (outubro 2024)
  - `claude-3-5-haiku-20241022` - Haiku mais recente
  - `claude-3-5-sonnet-20240620` - Sonnet (junho 2024)
  - `claude-3-opus-20240229` - Opus
  - `claude-3-sonnet-20240229` - Sonnet
  - `claude-3-haiku-20240307` - Haiku

#### AWS Bedrock
- ✅ **Atualizado modelo padrão**: `anthropic.claude-3-opus-20240229-v1:0` → `anthropic.claude-3-5-sonnet-20240620-v1:0`
- ✅ **Adicionado**: Claude 3.5 Sonnet v2 (mais recente)
- ✅ **Adicionado**: Claude 3.5 Haiku (outubro 2024)
- ✅ **Adicionado**: Amazon Titan Premier
- ✅ **Modelos disponíveis atualizados**:
  - `anthropic.claude-3-5-sonnet-20240620-v2:0` - Mais recente
  - `anthropic.claude-3-5-haiku-20241022-v1:0` - Haiku mais recente
  - `anthropic.claude-3-opus-20240229-v1:0` - Opus
  - `anthropic.claude-3-sonnet-20240229-v1:0` - Sonnet
  - `anthropic.claude-3-haiku-20240307-v1:0` - Haiku
  - `amazon.titan-text-premier-v1:0` - Titan Premier (mais recente)
  - `amazon.titan-text-express-v1` - Titan Express
  - `amazon.titan-text-lite-v1` - Titan Lite

#### Ollama
- ✅ **Atualizado modelo padrão**: `llama2` → `llama3.1`
- ✅ **Adicionados modelos mais recentes**:
  - `llama3.1` - Llama 3.1 (mais recente)
  - `llama3` - Llama 3
  - `mixtral` - Mixtral
  - `phi3` - Phi-3
  - `gemma2` - Gemma 2
  - `qwen2.5` - Qwen 2.5
  - `neural-chat` - Neural Chat

### 📝 Documentação
- ✅ Atualizado `README.md` com modelos mais recentes
- ✅ Atualizado `DEPLOY.md` com configurações atualizadas
- ✅ Adicionado `CHANGELOG.md` para rastreamento de mudanças

### 🔧 Arquivos Modificados
- `config.py` - Valores padrão atualizados
- `providers/openai_provider.py` - Lista de modelos atualizada
- `providers/anthropic_provider.py` - Lista de modelos atualizada
- `providers/bedrock_provider.py` - Lista de modelos atualizada
- `providers/ollama_provider.py` - Lista de modelos atualizada
- `README.md` - Documentação atualizada
- `DEPLOY.md` - Guia de deploy atualizado

## [1.0.0] - 2024-10-20

### 🎉 Lançamento Inicial
- Implementação inicial do portal e-BrAIn.Tech
- Suporte para múltiplos providers (OpenAI, Anthropic, AWS Bedrock, Ollama)
- Interface Streamlit moderna
- Sistema de histórico (90 interações)
- Arquitetura modular

