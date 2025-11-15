# Guia de Deploy - e-BrAIn.Tech

Este documento fornece instruções detalhadas para fazer deploy da aplicação e-BrAIn.Tech no Streamlit Cloud.

## 📋 Pré-requisitos

1. Conta no GitHub, GitLab ou Bitbucket
2. Repositório Git com o código da aplicação
3. Conta no Streamlit Cloud (gratuita)
4. API Keys dos providers que deseja usar

## 🚀 Deploy Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que seu repositório contém:
- ✅ `app.py` na raiz
- ✅ `requirements.txt` atualizado
- ✅ `config.py` configurado
- ✅ Todos os módulos necessários (`providers/`, `utils/`)

### 2. Criar Conta no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Clique em "Sign in"
3. Autorize com GitHub/GitLab/Bitbucket
4. Permita acesso aos seus repositórios

### 3. Fazer Deploy Inicial

1. No dashboard, clique em **"New app"**
2. Preencha:
   - **Repository**: Selecione seu repositório
   - **Branch**: `main` (ou sua branch principal)
   - **Main file path**: `app.py`
3. Clique em **"Deploy!"**

### 4. Configurar Secrets (Variáveis de Ambiente)

Após o deploy inicial:

1. Na página da aplicação, clique no menu **⋮** (três pontos)
2. Selecione **"Settings"**
3. Vá para a aba **"Secrets"**
4. Cole o seguinte template e preencha com suas credenciais:

```toml
# ============================================
# e-BrAIn.Tech - Configuração de Secrets
# ============================================

# OpenAI (Opcional - configure se quiser usar)
# Modelos disponíveis: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4o"

# Anthropic/Claude (Opcional - configure se quiser usar)
# Modelos disponíveis: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, claude-3-opus-20240229
ANTHROPIC_API_KEY = "sk-ant-..."
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"

# AWS Bedrock (Opcional - configure se quiser usar)
# Modelos disponíveis: anthropic.claude-3-5-sonnet-20240620-v2:0, anthropic.claude-3-5-haiku-20241022-v1:0
AWS_ACCESS_KEY_ID = "AKIA..."
AWS_SECRET_ACCESS_KEY = "wJalr..."
AWS_REGION = "us-east-1"
AWS_BEDROCK_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Ollama (Não funciona no Streamlit Cloud - apenas local)
# OLLAMA_BASE_URL = "http://localhost:11434"
# OLLAMA_MODEL = "llama2"

# Configurações Gerais
MAX_HISTORY = "90"
HISTORY_FILE = "history.json"
```

5. Clique em **"Save"**
6. A aplicação será reiniciada automaticamente

### 5. Verificar Deploy

1. Aguarde alguns segundos para a aplicação reiniciar
2. Acesse a URL fornecida (ex: `https://seu-app.streamlit.app`)
3. Verifique se:
   - A aplicação carrega corretamente
   - Os providers configurados aparecem como disponíveis na sidebar
   - É possível enviar mensagens e receber respostas

## 🔧 Configuração Avançada

### Personalizar URL

1. Em Settings → General
2. Clique em "Edit app URL"
3. Escolha uma URL personalizada (se disponível)

### Configurar Domínio Customizado

1. Em Settings → General
2. Adicione seu domínio customizado
3. Configure DNS conforme instruções

### Ajustar Recursos

Por padrão, o Streamlit Cloud oferece recursos limitados. Para mais recursos:
- Considere o plano pago do Streamlit Cloud
- Ou faça deploy em outro serviço (Heroku, AWS, etc.)

## 🐛 Troubleshooting

### Erro: "Module not found"

**Solução**: Verifique se todas as dependências estão em `requirements.txt`

### Erro: "API Key not configured"

**Solução**: 
1. Verifique se as Secrets estão configuradas corretamente
2. Certifique-se de que os nomes das variáveis estão corretos
3. Reinicie a aplicação após salvar as Secrets

### Erro: "Provider not available"

**Solução**:
1. Verifique se as credenciais estão corretas
2. Teste as credenciais localmente primeiro
3. Verifique se há limites de API atingidos

### Aplicação não atualiza após mudanças

**Solução**:
1. Verifique se fez commit e push das mudanças
2. Force um redeploy em Settings → General → "Reboot app"

### Ollama não funciona

**Causa**: Ollama requer um serviço local rodando, não disponível no Streamlit Cloud padrão.

**Solução**: Use Ollama apenas em deploy local ou em servidor próprio.

## 📊 Monitoramento

### Logs

1. Na página da aplicação, clique em "Manage app"
2. Vá para "Logs" para ver logs em tempo real
3. Útil para debug de erros

### Métricas

- Visualize uso de recursos
- Monitore performance
- Identifique problemas

## 🔄 Atualizações

Para atualizar a aplicação:

1. Faça commit e push das mudanças para o repositório
2. O Streamlit Cloud detecta automaticamente e faz redeploy
3. Ou force um redeploy manual em Settings

## 🔒 Segurança

### Boas Práticas

1. ✅ **Nunca** commite secrets no código
2. ✅ Use sempre as Secrets do Streamlit Cloud
3. ✅ Rotacione API keys regularmente
4. ✅ Monitore uso de API para detectar abusos
5. ✅ Use diferentes keys para desenvolvimento e produção

### Limites de Rate

Configure limites de rate nos providers para evitar custos excessivos:
- OpenAI: Configure limites na dashboard
- Anthropic: Configure limites na dashboard
- AWS: Use IAM policies para limitar uso

## 📝 Checklist de Deploy

Antes de fazer deploy, verifique:

- [ ] Código testado localmente
- [ ] `requirements.txt` atualizado
- [ ] Todas as dependências listadas
- [ ] Secrets configuradas no Streamlit Cloud
- [ ] API keys válidas e com créditos
- [ ] `.gitignore` configurado (não commitar secrets)
- [ ] README.md atualizado
- [ ] Documentação completa

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs da aplicação
2. Teste localmente primeiro
3. Consulte a documentação do Streamlit Cloud
4. Abra uma issue no repositório

## 📚 Recursos Adicionais

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Documentação Streamlit](https://docs.streamlit.io/)

