"""Main FastAPI application for Contax Brain.tech portal."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os

from config import settings
from llm_service import llm_service

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Portal inteligente com integração LLM para diversas possibilidades"
)

# Create static and templates directories if they don't exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Request/Response models
class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request model."""
    messages: List[ChatMessage]
    stream: bool = False
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class DocumentAnalysisRequest(BaseModel):
    """Document analysis request model."""
    document_text: str
    query: str


class CodeGenerationRequest(BaseModel):
    """Code generation request model."""
    description: str
    language: str = "python"


class CodeReviewRequest(BaseModel):
    """Code review request model."""
    code: str
    language: str = "python"


class DataAnalysisRequest(BaseModel):
    """Data analysis request model."""
    data: str
    query: str


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main portal page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
            "app_version": settings.app_version
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "llm_configured": bool(settings.openai_api_key)
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat with the LLM.
    
    Args:
        request: ChatRequest with messages and options
        
    Returns:
        JSON response with LLM reply or streaming response
    """
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        if request.stream:
            async def generate():
                async for chunk in await llm_service.chat(
                    messages=messages,
                    stream=True,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        else:
            result = await llm_service.chat(
                messages=messages,
                stream=False,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@app.post("/api/analyze-document")
async def analyze_document(request: DocumentAnalysisRequest):
    """
    Analyze a document and answer questions about it.
    
    Args:
        request: DocumentAnalysisRequest with document text and query
        
    Returns:
        JSON response with analysis results
    """
    try:
        result = await llm_service.analyze_document(
            document_text=request.document_text,
            query=request.query
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")


@app.post("/api/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """
    Generate code based on a description.
    
    Args:
        request: CodeGenerationRequest with description and language
        
    Returns:
        JSON response with generated code
    """
    try:
        result = await llm_service.generate_code(
            description=request.description,
            language=request.language
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")


@app.post("/api/review-code")
async def review_code(request: CodeReviewRequest):
    """
    Review code and provide suggestions.
    
    Args:
        request: CodeReviewRequest with code and language
        
    Returns:
        JSON response with review results
    """
    try:
        result = await llm_service.review_code(
            code=request.code,
            language=request.language
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reviewing code: {str(e)}")


@app.post("/api/analyze-data")
async def analyze_data(request: DataAnalysisRequest):
    """
    Analyze data and provide insights.
    
    Args:
        request: DataAnalysisRequest with data and query
        
    Returns:
        JSON response with analysis results
    """
    try:
        result = await llm_service.analyze_data(
            data=request.data,
            query=request.query
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
