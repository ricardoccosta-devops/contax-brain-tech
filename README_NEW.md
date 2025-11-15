# 🧠 e-BrAIn.Tech - Portal do Centro de Excelência em IA

**Versão 2.0 - Arquitetura Modular Completa**

O e-BrAIn.Tech é o portal oficial do Centro de Excelência em Inteligência Artificial da ContaX-Brain-Tech. Ele permite acesso integrado e contextual a múltiplos modelos de IA, oferecendo funcionalidades de revisão de código, geração de texto, sumarização, criação de imagens, speech-to-text e muito mais.

Com arquitetura modular e suporte a múltiplos providers de LLM, o portal oferece flexibilidade total, histórico das últimas 90 interações e uma experiência amigável e eficiente.

## 🏗️ Arquitetura

A aplicação segue os princípios de **Clean Architecture** com separação clara de responsabilidades:

```
app/
├── core/                    # Interfaces e abstrações centrais
│   ├── llm_interface.py     # Interface abstrata para providers
│   ├── context_manager.py   # Gerenciamento de contexto
│   ├── history_manager.py   # Histórico em SQLite
│   └── config_loader.py     # Carregamento de configurações
├── providers/               # Implementações de providers
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   ├── meta_provider.py
│   ├── ollama_provider.py
│   ├── bedrock_provider.py
│   ├── google_provider.py
│   └── provider_factory.py
├── features/                # Funcionalidades modulares
│   ├── chat.py
│   ├── code_review.py
│   ├── summarizer.py
│   ├── stt.py
│   └── image_generation.py
└── frontend/                # Interface Streamlit
    └── main_app.py
```

## 🚀 Características

### Providers Suportados

- ✅ **OpenAI** - GPT-4o, GPT-4 Turbo, DALL-E, Whisper
- ✅ **Anthropic** - Claude 3.5 Sonnet, Claude 3 Opus
- ✅ **Meta** - LLaMA 3.1 (via Ollama ou API)
- ✅ **Ollama** - Modelos locais (Llama, Mistral, etc.)
- ✅ **AWS Bedrock** - Claude via Bedrock
- ✅ **Google** - Gemini 1.5 Pro

### Funcionalidades

1. **💬 Chat IA** - Conversação contextual com IA
2. **🔍 Code Reviewer** - Revisão detalhada de código
3. **📝 Summarizer** - Sumarização de textos longos
4. **🎤 Speech-to-Text** - Transcrição de áudio
5. **🎨 Image Generator** - Geração de imagens via DALL-E
6. **📊 Histórico** - Visualização de interações anteriores
7. **⚙️ Configurações** - Gerenciamento de configurações

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Docker (opcional, para containerização)
- Credenciais para os providers desejados

## 🔧 Instalação

### Opção 1: Instalação Local

1. Clone o repositório:
```bash
git clone <repository-url>
cd contax-brain
```

2. Crie ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale dependências:
```bash
pip install -r requirements.txt
```

4. Configure variáveis de ambiente (crie `.env`):
```env
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Meta/Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# AWS Bedrock
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0

# Google
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-1.5-pro
```

5. Execute a aplicação:
```bash
streamlit run main.py
```

### Opção 2: Docker

1. Configure variáveis de ambiente no `.env`

2. Execute com Docker Compose:
```bash
docker-compose up -d
```

3. Acesse em `http://localhost:8501`

## 📖 Uso

### Chat IA

1. Selecione um provider na sidebar
2. Vá para a aba "💬 Chat IA"
3. Digite sua mensagem e pressione Enter
4. A IA responderá mantendo o contexto da conversa

### Code Reviewer

1. Vá para a aba "🔍 Code Reviewer"
2. Cole seu código
3. Selecione a linguagem (opcional)
4. Clique em "Revisar Código"

### Summarizer

1. Vá para a aba "📝 Summarizer"
2. Cole o texto a ser sumarizado
3. Ajuste o comprimento máximo
4. Clique em "Gerar Resumo"

### Speech-to-Text

1. Vá para a aba "🎤 Speech-to-Text"
2. Faça upload de arquivo de áudio
3. Clique em "Transcrever Áudio"

### Image Generator

1. Vá para a aba "🎨 Image Generator"
2. Descreva a imagem desejada
3. Selecione o tamanho
4. Clique em "Gerar Imagem"

## 🔒 Segurança

- ✅ Credenciais nunca são hardcoded
- ✅ Variáveis de ambiente para configuração
- ✅ Suporte a Secrets Manager no Streamlit Cloud
- ✅ Histórico armazenado localmente (SQLite)

## 🧪 Testes

Para testar um provider isoladamente:

```python
from app.providers.openai_provider import OpenAIProvider
from app.core.llm_interface import LLMMessage, TaskType

provider = OpenAIProvider()
if provider.is_available():
    messages = [LLMMessage(role="user", content="Olá!")]
    response = provider.generate_text(messages, TaskType.CHAT)
    print(response.content)
```

## 📚 Documentação Adicional

- `ARCHITECTURE.md` - Detalhes da arquitetura
- `DEPLOY.md` - Guia de deploy no Streamlit Cloud
- `CHANGELOG.md` - Histórico de mudanças

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é propriedade da Twinn/ContaX.

## 🆘 Suporte

Para suporte, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório.

---

**e-BrAIn.Tech** - Portal do Centro de Excelência em IA | ContaX-Brain-Tech

