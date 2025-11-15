# API Documentation - Contax Brain.tech Portal

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API uses server-side OpenAI API key configuration. No user authentication is required.

## Endpoints

### Health Check
Check if the service is running and configured properly.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Contax Brain.tech",
  "version": "1.0.0",
  "llm_configured": true
}
```

---

### Chat
General purpose chat with the AI assistant.

**Endpoint:** `POST /api/chat`

**Request Body:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "stream": false,
  "temperature": 0.7,
  "max_tokens": null
}
```

**Parameters:**
- `messages` (array, required): Array of message objects with `role` and `content`
- `stream` (boolean, optional): Enable streaming responses. Default: false
- `temperature` (float, optional): Sampling temperature (0-2). Default: 0.7
- `max_tokens` (integer, optional): Maximum tokens in response

**Response:**
```json
{
  "content": "Hello! I'm doing well, thank you for asking...",
  "model": "gpt-4-turbo-preview",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

---

### Analyze Document
Analyze documents and answer questions about them.

**Endpoint:** `POST /api/analyze-document`

**Request Body:**
```json
{
  "document_text": "This is the content of the document...",
  "query": "What is this document about?"
}
```

**Parameters:**
- `document_text` (string, required): The text content of the document
- `query` (string, required): Question or analysis request about the document

**Response:**
```json
{
  "content": "This document is about...",
  "model": "gpt-4-turbo-preview",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 50,
    "total_tokens": 200
  }
}
```

---

### Generate Code
Generate code based on natural language description.

**Endpoint:** `POST /api/generate-code`

**Request Body:**
```json
{
  "description": "Create a function that sorts a list of numbers",
  "language": "python"
}
```

**Parameters:**
- `description` (string, required): Description of what the code should do
- `language` (string, optional): Programming language. Options: python, javascript, java, csharp, go, rust. Default: python

**Response:**
```json
{
  "content": "Here's a Python function that sorts a list of numbers:\n\n```python\ndef sort_numbers(numbers):\n    return sorted(numbers)\n```",
  "model": "gpt-4-turbo-preview",
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 40,
    "total_tokens": 60
  }
}
```

---

### Review Code
Get a code review with suggestions for improvement.

**Endpoint:** `POST /api/review-code`

**Request Body:**
```json
{
  "code": "def hello():\n    print('hello')",
  "language": "python"
}
```

**Parameters:**
- `code` (string, required): The code to review
- `language` (string, optional): Programming language. Options: python, javascript, java, csharp, go, rust. Default: python

**Response:**
```json
{
  "content": "Code Review:\n\n1. Function naming: The function name 'hello' is descriptive...",
  "model": "gpt-4-turbo-preview",
  "usage": {
    "prompt_tokens": 30,
    "completion_tokens": 100,
    "total_tokens": 130
  }
}
```

---

### Analyze Data
Analyze data and provide insights.

**Endpoint:** `POST /api/analyze-data`

**Request Body:**
```json
{
  "data": "Name,Age\nJohn,30\nMary,25\nBob,35",
  "query": "What is the average age?"
}
```

**Parameters:**
- `data` (string, required): The data to analyze (CSV, JSON, or text format)
- `query` (string, required): The analysis request or question

**Response:**
```json
{
  "content": "Based on the provided data, the average age is 30 years...",
  "model": "gpt-4-turbo-preview",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 40,
    "total_tokens": 90
  }
}
```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters or missing API key
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting
The service uses OpenAI's API, which has its own rate limits. Please refer to OpenAI's documentation for current limits.

## Examples

### cURL Example - Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is Python?"}
    ],
    "temperature": 0.7
  }'
```

### Python Example - Generate Code
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate-code",
    json={
        "description": "Create a factorial function",
        "language": "python"
    }
)

print(response.json()["content"])
```

### JavaScript Example - Analyze Document
```javascript
fetch('http://localhost:8000/api/analyze-document', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    document_text: 'Sample document content...',
    query: 'What are the main points?'
  })
})
.then(response => response.json())
.then(data => console.log(data.content));
```

## Web Interface
The portal also provides a web interface accessible at `http://localhost:8000` with all features available through an intuitive UI.
