# e-BrAIn.Tech - Portal de CoE de IA

Portal de integração de IA que fornece acesso a múltiplos provedores de LLM (Large Language Models), incluindo OpenAI, Anthropic (Claude), AWS Bedrock e Ollama.

## 🚀 Características

- **Múltiplos Providers**: Suporte para OpenAI, Anthropic, AWS Bedrock e Ollama
- **Consciência Contextual**: Mantém o contexto das interações
- **Seleção de Modelos**: Escolha entre diferentes tipos de modelos:
  - 🔍 Code Review: Feedback detalhado sobre código
  - ✍️ Text Completion: Geração de texto coerente
  - 📝 Summarization: Resumos concisos
  - 🎤 Speech-to-Text: Conversão de fala em texto
  - 🎨 Image Creation: Geração de imagens baseadas em prompts
- **Histórico de Interações**: Armazena as últimas 90 interações
- **Interface Amigável**: Interface moderna e intuitiva com Streamlit
- **Arquitetura Modular**: Código bem organizado e modular

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Contas e credenciais para os providers que deseja usar:
  - OpenAI: API Key
  - Anthropic: API Key
  - AWS Bedrock: Access Key ID e Secret Access Key
  - Ollama: Serviço local (opcional)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd contax-brain
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:
```env
# OpenAI (Modelos mais recentes: GPT-4o, GPT-4o-mini, GPT-4 Turbo)
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4o

# Anthropic (Claude) - Modelos mais recentes: Claude 3.5 Sonnet, Claude 3.5 Haiku
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# AWS Bedrock (Modelos mais recentes: Claude 3.5 Sonnet, Claude 3.5 Haiku)
AWS_ACCESS_KEY_ID=seu_access_key_id_aqui
AWS_SECRET_ACCESS_KEY=seu_secret_access_key_aqui
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Configurações Gerais
MAX_HISTORY=90
HISTORY_FILE=history.json
```

**Nota**: Você não precisa configurar todos os providers. Configure apenas os que deseja usar.

## 🏃 Executando Localmente

Execute a aplicação Streamlit:
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## ☁️ Deploy no Streamlit Cloud

### Passo 1: Preparar o Repositório

1. Certifique-se de que seu código está em um repositório Git (GitHub, GitLab ou Bitbucket)
2. Verifique se o arquivo `requirements.txt` está atualizado
3. Certifique-se de que o arquivo `app.py` está na raiz do projeto

### Passo 2: Criar Conta no Streamlit Cloud

1. Acesse [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Faça login com sua conta GitHub/GitLab/Bitbucket
3. Autorize o Streamlit Cloud a acessar seus repositórios

### Passo 3: Deploy da Aplicação

1. No dashboard do Streamlit Cloud, clique em "New app"
2. Selecione:
   - **Repository**: Seu repositório
   - **Branch**: Branch principal (geralmente `main` ou `master`)
   - **Main file path**: `app.py`
3. Clique em "Deploy!"

### Passo 4: Configurar Variáveis de Ambiente

Após o deploy inicial, configure as variáveis de ambiente:

1. No dashboard do Streamlit Cloud, clique na sua aplicação
2. Vá em "Settings" (⚙️) → "Secrets"
3. Adicione as variáveis de ambiente no formato TOML:

```toml
# OpenAI
OPENAI_API_KEY = "sua_chave_openai_aqui"
OPENAI_MODEL = "gpt-4"

# Anthropic
ANTHROPIC_API_KEY = "sua_chave_anthropic_aqui"
ANTHROPIC_MODEL = "claude-3-opus-20240229"

# AWS Bedrock
AWS_ACCESS_KEY_ID = "seu_access_key_id_aqui"
AWS_SECRET_ACCESS_KEY = "seu_secret_access_key_aqui"
AWS_REGION = "us-east-1"
AWS_BEDROCK_MODEL = "anthropic.claude-3-opus-20240229-v1:0"

# Ollama (geralmente não funciona no Streamlit Cloud, apenas local)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"

# Configurações Gerais
MAX_HISTORY = "90"
HISTORY_FILE = "history.json"
```

4. Salve as configurações
5. A aplicação será reiniciada automaticamente

### Passo 5: Acessar a Aplicação

Após o deploy, você receberá uma URL única para sua aplicação, por exemplo:
`https://seu-app.streamlit.app`

## 📁 Estrutura do Projeto

```
contax-brain/
├── app.py                      # Aplicação principal Streamlit
├── config.py                   # Configurações centralizadas
├── requirements.txt            # Dependências Python
├── README.md                   # Documentação
├── .streamlit/
│   └── config.toml            # Configurações do Streamlit
├── providers/                  # Módulos de providers
│   ├── __init__.py
│   ├── base.py                # Classe base abstrata
│   ├── openai_provider.py     # Provider OpenAI
│   ├── anthropic_provider.py  # Provider Anthropic
│   ├── bedrock_provider.py    # Provider AWS Bedrock
│   └── ollama_provider.py     # Provider Ollama
└── utils/                      # Utilitários
    ├── __init__.py
    ├── history.py             # Gerenciamento de histórico
    └── provider_factory.py    # Factory de providers
```

## 🔌 Adicionando um Novo Provider

Para adicionar um novo provider de LLM:

1. Crie um novo arquivo em `providers/` (ex: `providers/novo_provider.py`)
2. Herde da classe `BaseProvider` em `providers/base.py`
3. Implemente os métodos obrigatórios:
   - `is_available()`: Verifica se o provider está configurado
   - `chat_completion()`: Gera respostas
   - `list_models()`: Lista modelos disponíveis
4. Adicione o provider ao `ProviderFactory` em `utils/provider_factory.py`
5. Adicione as variáveis de ambiente necessárias em `config.py`

Exemplo:
```python
from providers.base import BaseProvider, Message, ModelType

class NovoProvider(BaseProvider):
    def __init__(self):
        super().__init__("Novo Provider")
        # Inicialização
    
    def is_available(self) -> bool:
        # Verifica disponibilidade
        pass
    
    def chat_completion(self, messages, model_type, **kwargs):
        # Implementa geração de respostas
        pass
    
    def list_models(self):
        # Lista modelos
        pass
```

## 🔒 Segurança

- **Nunca** commite arquivos `.env` ou credenciais no Git
- Use as Secrets do Streamlit Cloud para variáveis sensíveis
- Mantenha suas API keys seguras e rotacione-as regularmente
- O arquivo `history.json` pode conter dados sensíveis - considere criptografá-lo em produção

## 📝 Notas Importantes

- **Ollama**: Funciona apenas localmente ou em servidores onde o serviço está rodando. Não funciona no Streamlit Cloud padrão.
- **AWS Bedrock**: Requer credenciais AWS válidas e acesso ao serviço Bedrock na região configurada.
- **Histórico**: O histórico é armazenado localmente em `history.json`. No Streamlit Cloud, cada instância tem seu próprio histórico.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é propriedade da Twinn/ContaX.

## 🆘 Suporte

Para suporte, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório.
