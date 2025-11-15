// Chat history
let chatHistory = [];

// Tab management
function openTab(tabName) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    // Remove active class from all buttons
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    // Show selected tab and activate button
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Chat functionality
function addMessage(role, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to UI
    addMessage('user', message);
    chatHistory.push({ role: 'user', content: message });
    input.value = '';
    
    // Show loading
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = 'Pensando<span class="loading"></span>';
    document.getElementById('chat-messages').appendChild(loadingDiv);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                messages: chatHistory,
                stream: false,
                temperature: 0.7
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao processar mensagem');
        }
        
        const data = await response.json();
        loadingDiv.remove();
        
        addMessage('assistant', data.content);
        chatHistory.push({ role: 'assistant', content: data.content });
        
    } catch (error) {
        loadingDiv.remove();
        addMessage('system', `Erro: ${error.message}`);
        console.error('Chat error:', error);
    }
}

// Document analysis
async function analyzeDocument() {
    const docText = document.getElementById('doc-text').value.trim();
    const query = document.getElementById('doc-query').value.trim();
    const resultDiv = document.getElementById('doc-result');
    
    if (!docText || !query) {
        resultDiv.textContent = 'Por favor, forneça o texto do documento e uma pergunta.';
        resultDiv.style.display = 'block';
        return;
    }
    
    resultDiv.textContent = 'Analisando documento...';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/analyze-document', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                document_text: docText,
                query: query
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao analisar documento');
        }
        
        const data = await response.json();
        resultDiv.textContent = data.content;
        
    } catch (error) {
        resultDiv.textContent = `Erro: ${error.message}`;
        console.error('Document analysis error:', error);
    }
}

// Code generation
async function generateCode() {
    const description = document.getElementById('code-desc').value.trim();
    const language = document.getElementById('code-lang').value;
    const resultDiv = document.getElementById('code-gen-result');
    
    if (!description) {
        resultDiv.textContent = 'Por favor, descreva o que o código deve fazer.';
        resultDiv.style.display = 'block';
        return;
    }
    
    resultDiv.textContent = 'Gerando código...';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/generate-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                description: description,
                language: language
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao gerar código');
        }
        
        const data = await response.json();
        resultDiv.textContent = data.content;
        
    } catch (error) {
        resultDiv.textContent = `Erro: ${error.message}`;
        console.error('Code generation error:', error);
    }
}

// Code review
async function reviewCode() {
    const code = document.getElementById('review-code').value.trim();
    const language = document.getElementById('review-lang').value;
    const resultDiv = document.getElementById('code-review-result');
    
    if (!code) {
        resultDiv.textContent = 'Por favor, forneça o código para revisar.';
        resultDiv.style.display = 'block';
        return;
    }
    
    resultDiv.textContent = 'Revisando código...';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/review-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao revisar código');
        }
        
        const data = await response.json();
        resultDiv.textContent = data.content;
        
    } catch (error) {
        resultDiv.textContent = `Erro: ${error.message}`;
        console.error('Code review error:', error);
    }
}

// Data analysis
async function analyzeData() {
    const data = document.getElementById('data-input').value.trim();
    const query = document.getElementById('data-query').value.trim();
    const resultDiv = document.getElementById('data-result');
    
    if (!data || !query) {
        resultDiv.textContent = 'Por favor, forneça os dados e a análise solicitada.';
        resultDiv.style.display = 'block';
        return;
    }
    
    resultDiv.textContent = 'Analisando dados...';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/analyze-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: data,
                query: query
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao analisar dados');
        }
        
        const result = await response.json();
        resultDiv.textContent = result.content;
        
    } catch (error) {
        resultDiv.textContent = `Erro: ${error.message}`;
        console.error('Data analysis error:', error);
    }
}

// Allow Enter key to send chat messages (with Shift+Enter for new line)
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
});
