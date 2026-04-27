import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncpg
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form, Query, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import openai
import logging
from repository.dog_chats_repository import DogChatsRepository
from repository.user_repository import UserRepository
from repository.pet_repository import PetRepository
from entity.dog_chat import DogChat
from llm.openai import OpenAIChatService
from datetime import date
from llm.ollama.chat import DogChatSystem
from repository.dog_docs_repository import DogDocsRepository
from repository.dog_meal_repository import DogMealRepository
from repository.dog_snack_repository import DogSnackRepository
from repository.dog_walk_repository import DogWalkRepository
from repository.dog_temperature_repository import DogTemperatureRepository
from llm.model import get_model
from contextlib import asynccontextmanager
from rag.processor import DocumentProcessor
import shutil
from pathlib import Path
from rag.loader import DocumentLoader
import asyncio
import signal
import uvicorn
from logging.handlers import RotatingFileHandler
import markdown
from datetime import datetime
from repository.prompt_template_repository import PromptTemplateRepository
from repository.pulse_repository import PulseRepository
from repository.respiration_repository import RespirationRepository

# 로깅 설정
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

# RotatingFileHandler 설정
file_handler = RotatingFileHandler(
    filename=os.path.join(log_dir, 'app.log'),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,  # 최대 5개의 백업 파일 유지
    encoding='utf-8'
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # PostgreSQL 연결 풀 생성
        app.state.pool = await asyncpg.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            database=os.getenv("DB_NAME", "dailypet"),
            min_size=5,
            max_size=20
        )
        
        # Repository 초기화
        app.state.user_repo = UserRepository(app.state.pool)
        app.state.pet_repo = PetRepository(app.state.pool)
        app.state.dog_docs_repo = DogDocsRepository(app.state.pool)
        app.state.dog_chats_repo = DogChatsRepository(app.state.pool)
        app.state.dog_meal_repo = DogMealRepository(app.state.pool)
        app.state.dog_snack_repo = DogSnackRepository(app.state.pool)
        app.state.dog_walk_repo = DogWalkRepository(app.state.pool)
        app.state.dog_temperature_repo = DogTemperatureRepository(app.state.pool)
        app.state.prompt_template_repo = PromptTemplateRepository(app.state.pool)
        app.state.pulse_repo = PulseRepository(app.state.pool)
        app.state.respiration_repo = RespirationRepository(app.state.pool)
        
        # LLM 시스템 초기화
        app.state.ollama_chat_system = DogChatSystem(
            docs_repo=app.state.dog_docs_repo,
            chats_repo=app.state.dog_chats_repo,
            profile_repo=app.state.pet_repo,
            dog_meal_repo=app.state.dog_meal_repo,
            dog_snack_repo=app.state.dog_snack_repo,
            dog_walk_repo=app.state.dog_walk_repo,
            dog_temperature_repo=app.state.dog_temperature_repo,
            pulse_repo=app.state.pulse_repo,
            respiration_repo=app.state.respiration_repo
        )
        
        # OpenAI 채팅 서비스 초기화
        app.state.openai_chat_service = OpenAIChatService(
            docs_repo=app.state.dog_docs_repo,
            pet_repo=app.state.pet_repo,
            dog_chats_repo=app.state.dog_chats_repo,
            dog_meal_repo=app.state.dog_meal_repo,
            dog_snack_repo=app.state.dog_snack_repo,
            dog_walk_repo=app.state.dog_walk_repo,
            dog_temperature_repo=app.state.dog_temperature_repo,
            pulse_repo=app.state.pulse_repo,
            respiration_repo=app.state.respiration_repo
        )
        
        yield
        
    finally:
        # Shutdown
        if hasattr(app.state, 'pool'):
            await app.state.pool.close()

# Initialize FastAPI app
app = FastAPI(title="Dog LLM API", lifespan=lifespan)

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory="resource/static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="resource/templates")

# OpenAI API 키 확인
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logger.error("OPENAI_API_KEY가 설정되지 않았습니다.")
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
openai.api_key = openai_api_key

# Initialize repositories
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "dog_llm"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "active1004")
}

class MessageRequest(BaseModel):
    message: str
    k: int = 3

class ChatRequest(BaseModel):
    dog_id: int
    message: str

class ChatResponse(BaseModel):
    response: str

class DogMealRequest(BaseModel):
    dog_id: int
    meal_time: datetime
    food_type: str
    amount: float
    notes: Optional[str] = None

class DogSnackRequest(BaseModel):
    dog_id: int
    snack_time: datetime
    snack_type: str
    amount: float
    notes: Optional[str] = None

class DogWalkRequest(BaseModel):
    dog_id: int
    start_time: datetime
    end_time: datetime
    distance: float
    notes: Optional[str] = None

class DogRespiratoryRateRequest(BaseModel):
    dog_id: int
    measured_at: datetime
    rate: int
    notes: Optional[str] = None

class DogHeartRateRequest(BaseModel):
    dog_id: int
    measured_at: datetime
    rate: int
    notes: Optional[str] = None

class DogTemperatureRequest(BaseModel):
    dog_id: int
    measured_at: datetime
    temperature: float
    notes: Optional[str] = None

# 프롬프트 템플릿 관련 모델
class PromptTemplateRequest(BaseModel):
    name: str
    content: str

class PromptChatRequest(BaseModel):
    dog_id: int
    message: str
    template_id: int

class UserRequest(BaseModel):
    uid: str = Query(default="", description="사용자 ID")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, params: UserRequest = Depends()):
    try:
        # 프로필 데이터 조회
        profiles = await app.state.pet_repo.get_all_pets()
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "profiles": profiles
            }
        )
    except Exception as e:
        logger.error(f"프로필 데이터 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@app.post("/dog/docs")
async def get_dog_docs(request: MessageRequest):
    try:
        # 질문의 임베딩 생성
        query_embedding = get_model().encode(request.message, normalize_embeddings=True)
        
        # 데이터베이스에서 유사한 문서 검색
        similar_docs = await app.state.dog_docs_repo.search_similar_docs(query_embedding, request.k)
        # content와 source만 포함하도록 수정
        similar_docs = [{"content": doc.content, "source": doc.source} for doc in similar_docs]
        
        return {
            "response": similar_docs
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"입베딩 DB 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="입베딩 DB 조회 중 오류가 발생했습니다.")

@app.post("/openai/chat")
async def chat_with_openai(request: ChatRequest):
    try:
        bot_response = await app.state.openai_chat_service.chat_with_dog(request.dog_id, request.message)
        return {"response": bot_response}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"채팅 처리 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="채팅 처리 중 오류가 발생했습니다.")

@app.post("/ollama/chat")
async def chat_with_ollama(request: ChatRequest):
    try:
        response = await app.state.ollama_chat_system.chat_with_dog(request.dog_id, request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"채팅 처리 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="채팅 처리 중 오류가 발생했습니다.")

@app.post("/ollama/chat/stream")
async def chat_with_ollama_stream(request: ChatRequest):
    """스트리밍 방식으로 Ollama 채팅을 처리합니다."""
    try:
        async def generate():
            async for chunk in app.state.ollama_chat_system.chat_with_dog_stream(request.dog_id, request.message):
                yield chunk
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            }
        )
    except Exception as e:
        logger.error(f"스트리밍 채팅 처리 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="스트리밍 채팅 처리 중 오류가 발생했습니다.")

@app.get("/rag", response_class=HTMLResponse)
async def rag_page(request: Request):
    return templates.TemplateResponse("rag.html", {"request": request})

@app.get("/doc", response_class=HTMLResponse)
async def docs_page(request: Request, source: str = None, loader_type: str = None):
    try:
        docs = []
        sources = await app.state.dog_docs_repo.get_distinct_sources()
        loader_types = []
        
        if source:
            loader_types = await app.state.dog_docs_repo.get_distinct_loader_types(source)
            if loader_type:
                docs = await app.state.dog_docs_repo.get_docs_by_source_and_loader(source, loader_type)
        
        return templates.TemplateResponse(
            "docs.html",
            {
                "request": request,
                "docs": docs,
                "sources": sources,
                "loader_types": loader_types,
                "selected_source": source or "",
                "selected_loader_type": loader_type or ""
            }
        )
    except Exception as e:
        logger.error(f"문서 목록 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@app.get("/api/loader-types/{source}")
async def get_loader_types(source: str):
    try:
        loader_types = await app.state.dog_docs_repo.get_distinct_loader_types(source)
        return {"loader_types": loader_types}
    except Exception as e:
        logger.error(f"로더 타입 목록 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), pdf_loader_type: str = Form(None)):
    try:
        # 임시 파일 저장
        temp_file = Path("temp") / file.filename
        temp_file.parent.mkdir(exist_ok=True)
        
        with temp_file.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 문서 로드
        loader = DocumentLoader(file.filename, pdf_loader_type)
        texts = loader.load_document(temp_file)
        
        # 문서 처리 및 저장
        processor = DocumentProcessor(loader)
        dog_docs = processor.process_document(texts, file.filename)
        
        # 각 문서를 데이터베이스에 저장
        for doc in dog_docs:
            await app.state.dog_docs_repo.create_doc(
                content=doc.content,
                embedding=doc.embedding,
                source=doc.source,
                loader_type=doc.loader_type
            )
        
        # 임시 파일 삭제
        temp_file.unlink()
        
        return {"message": "문서가 성공적으로 처리되었습니다.", "texts": texts}
    except Exception as e:
        logger.error(f"문서 업로드 중 오류 발생: {str(e)}")
        return {"error": str(e)}
    finally:
        file.file.close()

# /docs 디렉토리의 마크다운 파일 목록을 가져오는 함수
def get_markdown_files():
    docs_dir = Path("docs")
    markdown_files = []
    
    for file in docs_dir.glob("*.md"):
        # 파일 생성 시간을 가져옴
        created_time = datetime.fromtimestamp(file.stat().st_ctime)
        markdown_files.append({
            "name": file.name,
            "path": str(file),
            "created_time": created_time
        })
    
    # 생성 시간 순으로 정렬 (최신순)
    return sorted(markdown_files, key=lambda x: x["created_time"], reverse=True)

@app.get("/docs/llm-rag", response_class=HTMLResponse)
async def read_llm_rag_docs(request: Request):
    # 마크다운 파일 목록을 가져옴
    markdown_files = get_markdown_files()
    
    # 기본적으로 첫 번째 파일을 선택
    selected_file = markdown_files[0] if markdown_files else None
    content = ""
    
    if selected_file:
        with open(selected_file["path"], "r", encoding="utf-8") as f:
            content = f.read()
            content = markdown.markdown(content)
    
    return templates.TemplateResponse(
        "llm_rag_docs.html",
        {
            "request": request,
            "markdown_files": markdown_files,
            "selected_file": selected_file,
            "content": content
        }
    )

@app.get("/docs/llm-rag/{filename}", response_class=HTMLResponse)
async def read_markdown_file(request: Request, filename: str):
    # 마크다운 파일 목록을 가져옴
    markdown_files = get_markdown_files()
    
    # 선택된 파일 찾기
    selected_file = next((f for f in markdown_files if f["name"] == filename), None)
    content = ""
    
    if selected_file:
        with open(selected_file["path"], "r", encoding="utf-8") as f:
            content = f.read()
            content = markdown.markdown(content)
    
    return templates.TemplateResponse(
        "llm_rag_docs.html",
        {
            "request": request,
            "markdown_files": markdown_files,
            "selected_file": selected_file,
            "content": content
        }
    )

@app.get('/chat/history')
async def get_chat_history(request: Request):
    dog_id = int(request.query_params.get('dog_id'))
    provider = request.query_params.get('provider')
    cursor = request.query_params.get('cursor')  # 커서 기반 페이지네이션
    page_size = int(request.query_params.get('page_size', 10))
    
    if not dog_id or not provider:
        return JSONResponse({'error': '필수 파라미터가 누락되었습니다.'}, status_code=400)
    
    try:
        repository = app.state.dog_chats_repo
        
        # 커서 기반 페이지네이션 사용
        result = await repository.get_chats_by_pet_and_provider_cursor(
            dog_id=dog_id,
            llm_provider=provider,
            limit=page_size,
            cursor=cursor
        )
        
        chats = result['chats']
        next_cursor = result['next_cursor']
        has_more = result['has_more']
        
        # 채팅 이력 포맷팅
        formatted_chats = []
        for chat in chats:
            # AI 응답
            if chat.response:
                formatted_chats.append({
                    'role': 'assistant',
                    'content': chat.response,
                    'createdAt': chat.created_at.isoformat() if chat.created_at else None
                })
            # 사용자 메시지
            if chat.message:
                formatted_chats.append({
                    'role': 'user',
                    'content': chat.message,
                    'createdAt': chat.created_at.isoformat() if chat.created_at else None
                })
        
        return JSONResponse({
            'chats': formatted_chats,
            'hasMore': has_more,
            'nextCursor': next_cursor
        })
    except ValueError as e:
        logger.error(f"파라미터 변환 중 오류 발생: {str(e)}")
        return JSONResponse({'error': '잘못된 파라미터 형식입니다.'}, status_code=400)
    except Exception as e:
        logger.error(f"채팅 이력 조회 중 오류 발생: {str(e)}")
        return JSONResponse({'error': str(e)}, status_code=500)
    

@app.get("/prompt-templates", response_class=HTMLResponse)
async def prompt_templates_page(request: Request):
    """프롬프트 템플릿 관리 페이지를 렌더링합니다."""
    template_list = await request.app.state.prompt_template_repo.get_all()
    return templates.TemplateResponse("prompt_templates.html", {
        "request": request,
        "templates": template_list
    })

@app.get("/api/prompt_templates")
async def get_prompt_templates():
    """모든 프롬프트 템플릿을 조회합니다."""
    templates = await app.state.prompt_template_repo.get_all()
    return templates

@app.get("/api/prompt_templates/{template_id}")
async def get_prompt_template(template_id: int):
    """특정 프롬프트 템플릿을 조회합니다."""
    template = await app.state.prompt_template_repo.get_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")
    return template

@app.post("/api/prompt_templates")
async def create_prompt_template(template: PromptTemplateRequest):
    """새로운 프롬프트 템플릿을 생성합니다."""
    from entity.prompt_template import PromptTemplate
    new_template = PromptTemplate(
        name=template.name,
        content=template.content
    )
    template_id = await app.state.prompt_template_repo.create(new_template)
    return {"id": template_id}

@app.put("/api/prompt_templates/{template_id}")
async def update_prompt_template(template_id: int, template: PromptTemplateRequest):
    """프롬프트 템플릿을 수정합니다."""
    from entity.prompt_template import PromptTemplate
    existing = await app.state.prompt_template_repo.get_by_id(template_id)
    if not existing:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")
    
    updated = PromptTemplate(
        id=template_id,
        name=template.name,
        content=template.content
    )
    success = await app.state.prompt_template_repo.update(updated)
    if not success:
        raise HTTPException(status_code=500, detail="템플릿 수정에 실패했습니다.")
    return {"success": True}

@app.delete("/api/prompt_templates/{template_id}")
async def delete_prompt_template(template_id: int):
    """프롬프트 템플릿을 삭제합니다."""
    success = await app.state.prompt_template_repo.delete(template_id)
    if not success:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")
    return {"success": True}

@app.get("/prompt-chat", response_class=HTMLResponse)
async def prompt_chat_page(request: Request, params: UserRequest = Depends()):
    """프롬프트 템플릿 채팅 페이지를 렌더링합니다."""
    template_list = await request.app.state.prompt_template_repo.get_all()
    profiles = await request.app.state.pet_repo.get_all_pets()
    return templates.TemplateResponse("prompt_chat.html", {
        "request": request,
        "templates": template_list,
        "profiles": profiles
    })

@app.post("/api/prompt_chat")
async def chat_with_prompt_template(request: PromptChatRequest):
    """프롬프트 템플릿을 사용하여 채팅합니다."""
    try:
        # 프롬프트 템플릿 조회
        template = await app.state.prompt_template_repo.get_by_id(request.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")
        
        # 기존 Ollama 채팅 시스템 재사용
        chat_system = app.state.ollama_chat_system
        chat_system.prompt_template.template = template.content
        
        # 채팅 응답 생성
        response = await chat_system.chat_with_dog(request.dog_id, request.message)
        return {"response": response}
        
    except Exception as e:
        logger.error(f"프롬프트 템플릿 채팅 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prompt_chat/stream")
async def chat_with_prompt_template_stream(request: PromptChatRequest):
    """프롬프트 템플릿을 사용하여 스트리밍 방식으로 채팅합니다."""
    try:
        # 프롬프트 템플릿 조회
        template = await app.state.prompt_template_repo.get_by_id(request.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")
        
        async def generate():
            async for chunk in app.state.ollama_chat_system.chat_with_prompt_template_stream(
                request.dog_id, 
                request.message, 
                template.content
            ):
                yield chunk
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            }
        )
        
    except Exception as e:
        logger.error(f"프롬프트 템플릿 스트리밍 채팅 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 이벤트 루프 설정 (Python 3.14 호환)
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# 종료 시그널 핸들러
def handle_exit(sig, frame):
    logger.info("애플리케이션 종료 중...")
    loop.stop()
    sys.exit(0)

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        logger.info("애플리케이션 종료 중...")
        loop.stop()
    finally:
        loop.close() 