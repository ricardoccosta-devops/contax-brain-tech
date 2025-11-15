"""
e-BrAIn.Tech - Portal de CoE de IA
Aplicação principal Streamlit
"""
import streamlit as st
import uuid
from datetime import datetime
from typing import List, Dict
from providers.base import ModelType, Message
from utils.history import HistoryManager
from utils.provider_factory import ProviderFactory
import config

# Configuração da página
st.set_page_config(
    page_title="e-BrAIn.Tech - Portal de CoE de IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_provider" not in st.session_state:
    st.session_state.current_provider = None

if "current_model_type" not in st.session_state:
    st.session_state.current_model_type = ModelType.TEXT_COMPLETION

if "interaction_id" not in st.session_state:
    st.session_state.interaction_id = str(uuid.uuid4())

if "history_manager" not in st.session_state:
    st.session_state.history_manager = HistoryManager()

# Título e cabeçalho
st.title("🧠 e-BrAIn.Tech")
st.caption("Seu Portal de CoE de IA")

# Sidebar - Configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seleção de Provider
    available_providers = ProviderFactory.get_available_providers()
    provider_options = [name for name, available in available_providers.items() if available]
    
    if not provider_options:
        st.error("⚠️ Nenhum provider configurado. Configure as variáveis de ambiente.")
        st.stop()
    
    selected_provider_name = st.selectbox(
        "Selecione o Provider",
        options=provider_options,
        index=0
    )
    
    st.session_state.current_provider = ProviderFactory.get_provider(selected_provider_name)
    
    # Status dos providers
    st.subheader("Status dos Providers")
    for name, available in available_providers.items():
        status = "✅" if available else "❌"
        st.write(f"{status} {name}")
    
    # Seleção de Tipo de Modelo
    st.divider()
    st.subheader("Tipo de Modelo")
    
    model_types = {
        "🔍 Code Review": ModelType.CODE_REVIEW,
        "✍️ Text Completion": ModelType.TEXT_COMPLETION,
        "📝 Summarization": ModelType.SUMMARIZATION,
        "🎤 Speech-to-Text": ModelType.SPEECH_TO_TEXT,
        "🎨 Image Creation": ModelType.IMAGE_CREATION,
    }
    
    selected_model_label = st.selectbox(
        "Selecione o tipo de modelo",
        options=list(model_types.keys())
    )
    st.session_state.current_model_type = model_types[selected_model_label]
    
    # Descrição do tipo de modelo
    descriptions = {
        ModelType.CODE_REVIEW: "Obtenha feedback detalhado e sugestões sobre seu código",
        ModelType.TEXT_COMPLETION: "Gere texto coerente e contextualmente apropriado",
        ModelType.SUMMARIZATION: "Condense documentos longos em resumos concisos",
        ModelType.SPEECH_TO_TEXT: "Converta linguagem falada em texto escrito",
        ModelType.IMAGE_CREATION: "Gere imagens baseadas em prompts descritivos",
    }
    st.caption(descriptions[st.session_state.current_model_type])
    
    # Histórico
    st.divider()
    st.subheader("📜 Histórico")
    
    history = st.session_state.history_manager.get_history()
    st.write(f"Interações salvas: {len(history)}/{config.Config.MAX_HISTORY}")
    
    if st.button("🔄 Nova Conversa"):
        st.session_state.messages = []
        st.session_state.interaction_id = str(uuid.uuid4())
        st.rerun()
    
    if st.button("🗑️ Limpar Histórico"):
        if st.session_state.history_manager:
            st.session_state.history_manager.clear_history()
            st.success("Histórico limpo!")
            st.rerun()
    
    # Lista de interações anteriores
    if history:
        st.subheader("Interações Anteriores")
        for interaction in history[:10]:  # Mostra apenas as 10 mais recentes
            if st.button(
                f"📄 {interaction['title'][:50]}",
                key=f"hist_{interaction['id']}",
                use_container_width=True
            ):
                st.session_state.messages = interaction['messages']
                st.session_state.interaction_id = interaction['id']
                st.session_state.current_model_type = ModelType(interaction['model_type'])
                st.rerun()

# Área principal - Chat
st.header("💬 Conversa")

# Exibe mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image_url"):
            st.image(message["image_url"], caption="Imagem gerada")
        st.write(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    user_message = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Gera resposta
    with st.chat_message("assistant"):
        with st.spinner("Gerando resposta..."):
            try:
                # Converte mensagens para formato do provider
                provider_messages = [
                    Message(role=msg["role"], content=msg["content"])
                    for msg in st.session_state.messages
                ]
                
                # Chama o provider
                provider = st.session_state.current_provider
                if not provider:
                    st.error("Provider não selecionado")
                    st.stop()
                
                response = provider.chat_completion(
                    messages=provider_messages,
                    model_type=st.session_state.current_model_type
                )
                
                # Exibe resposta
                if response.get("image_url"):
                    st.image(response["image_url"], caption="Imagem gerada")
                
                assistant_message = {
                    "role": "assistant",
                    "content": response.get("content", ""),
                    "image_url": response.get("image_url"),
                    "timestamp": datetime.now().isoformat()
                }
                
                st.write(assistant_message["content"])
                st.session_state.messages.append(assistant_message)
                
                # Salva no histórico
                title = st.session_state.messages[0]["content"][:50] if st.session_state.messages else "Nova Conversa"
                st.session_state.history_manager.add_interaction(
                    interaction_id=st.session_state.interaction_id,
                    messages=st.session_state.messages,
                    provider=selected_provider_name,
                    model_type=st.session_state.current_model_type.value,
                    title=title
                )
                
            except Exception as e:
                error_msg = f"Erro: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().isoformat()
                })

# Footer
st.divider()
st.caption("e-BrAIn.Tech - Portal de CoE de IA | Mantém contexto das interações e armazena as últimas 90 interações")

