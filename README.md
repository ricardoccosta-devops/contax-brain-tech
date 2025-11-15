# Contax Brain.tech Portal

Portal inteligente com integração LLM (Large Language Model) para diversas possibilidades de automação e assistência com Inteligência Artificial.

## 🚀 Funcionalidades

O portal oferece múltiplas capacidades de IA integradas:

### 💬 Chat Geral
- Assistente de conversação inteligente
- Histórico de conversas mantido durante a sessão
- Interface intuitiva e responsiva

### 📄 Análise de Documentos
- Envie documentos em formato texto
- Faça perguntas sobre o conteúdo
- Obtenha resumos e insights automatizados

### ⚙️ Geração de Código
- Descreva o que você precisa em linguagem natural
- Suporte para múltiplas linguagens: Python, JavaScript, Java, C#, Go, Rust
- Código limpo e bem documentado

### 🔍 Revisão de Código
- Cole seu código para análise
- Receba feedback sobre qualidade, segurança e performance
- Sugestões de melhores práticas

### 📊 Análise de Dados
- Envie dados em formato CSV, JSON ou texto
- Solicite análises específicas
- Obtenha insights e estatísticas

## 🛠️ Tecnologias Utilizadas

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **IA**: OpenAI GPT-4
- **Servidor**: Uvicorn
- **Containerização**: Docker

## 📋 Pré-requisitos

- Python 3.9 ou superior
- Chave de API da OpenAI
- Docker (opcional, para deployment)

## 🔧 Instalação

### Método 1: Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/ricardoccosta-devops/contax-brain-tech.git
cd contax-brain-tech
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

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

5. Edite o arquivo `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sua_chave_aqui
```

6. Execute o servidor:
```bash
python main.py
```

7. Acesse o portal em: `http://localhost:8000`

### Método 2: Docker

1. Clone o repositório:
```bash
git clone https://github.com/ricardoccosta-devops/contax-brain-tech.git
cd contax-brain-tech
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Edite o arquivo `.env` e adicione sua chave da OpenAI

4. Execute com Docker Compose:
```bash
docker-compose up -d
```

5. Acesse o portal em: `http://localhost:8000`

## 📖 Uso

### API Endpoints

O portal expõe os seguintes endpoints REST:

#### Chat
```http
POST /api/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Olá!"}
  ],
  "stream": false,
  "temperature": 0.7
}
```

#### Análise de Documentos
```http
POST /api/analyze-document
Content-Type: application/json

{
  "document_text": "Texto do documento...",
  "query": "O que este documento diz sobre...?"
}
```

#### Geração de Código
```http
POST /api/generate-code
Content-Type: application/json

{
  "description": "Criar uma função que ordena uma lista",
  "language": "python"
}
```

#### Revisão de Código
```http
POST /api/review-code
Content-Type: application/json

{
  "code": "def exemplo():\n    pass",
  "language": "python"
}
```

#### Análise de Dados
```http
POST /api/analyze-data
Content-Type: application/json

{
  "data": "Nome,Idade\nJoão,30\nMaria,25",
  "query": "Qual a média de idade?"
}
```

#### Health Check
```http
GET /health
```

## 🏗️ Estrutura do Projeto

```
contax-brain-tech/
├── main.py                 # Aplicação FastAPI principal
├── config.py               # Configurações da aplicação
├── llm_service.py          # Serviço de integração com LLM
├── requirements.txt        # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
├── Dockerfile              # Dockerfile para containerização
├── docker-compose.yml      # Configuração Docker Compose
├── templates/
│   └── index.html          # Template HTML principal
├── static/
│   ├── style.css           # Estilos CSS
│   └── script.js           # JavaScript do frontend
└── README.md               # Este arquivo
```

## 🔒 Segurança

- As chaves de API devem ser mantidas em segredo
- Nunca commite o arquivo `.env` no repositório
- Use variáveis de ambiente para configurações sensíveis
- O portal valida todas as entradas do usuário

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👥 Autores

- Contax Brain.tech Team

## 🙏 Agradecimentos

- OpenAI pela API GPT-4
- FastAPI pela excelente framework
- Comunidade open source

## 📞 Suporte

Para suporte, envie um email para suporte@contaxbrain.tech ou abra uma issue no GitHub.

---

**Contax Brain.tech** - Powered by AI 🧠