from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.request_schema import PromptRequest,ApiKeyRequest
from core.cache import generate_cache_key
from db.session import get_db
from services.factory import get_llm_provider
import json, re
from models.models import CachedQuestion
# from models.models import CachedQuestion
import google.generativeai as genai


router = APIRouter()


@router.post("/api/validate-gemini-key")
async def validate_gemini_key(request: ApiKeyRequest):
    try:
        genai.configure(api_key=request.api_key)        
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("Hello")
        return {"valid": True, "message": "API key is valid"}
    
    except Exception as e:
        return {"valid": False, "message": "Invalid API key or service unavailable"}


@router.post("/validate-api-key")
async def validate_api_key(request: ApiKeyRequest):
    try:
        llm = get_llm_provider(request.model_name, request.api_key)
        is_valid = llm.validate_api_key()
        return is_valid
    except Exception as e:
        return {"valid": False, "message": "Invalid API key or service unavailable"}




@router.post("/generate-questions/")
async def generate_questions(request: PromptRequest, db: Session = Depends(get_db)):
    if not request.is_test:
        cache_key = generate_cache_key(request.prompt + request.model_name)
        cached = db.query(CachedQuestion).filter(CachedQuestion.cache_key == cache_key).first()
        if cached:
            print('Cache hit')
            cached.hit_count+=1
            db.commit()
            return {"questions": json.loads(cached.response_json)}

    try:
        print('Cache Miss')
        llm = get_llm_provider(request.model_name, request.api_key)
        questions = llm.generate(request.prompt)
        print('questions are ',questions)

        if not request.is_test:
            db.add(CachedQuestion(
                cache_key=cache_key,
                name=request.name,
                type=request.type,
                model_name=request.model_name,
                response_json=json.dumps(questions)
            ))
            db.commit()
        return {"questions": questions}
    except Exception as e:
        print('Error is ',str(e))
        return {"error": str(e)}



@router.get("/popular-content/")
def get_popular_content(db: Session = Depends(get_db)):
    results = (
        db.query(CachedQuestion.type, CachedQuestion.name, CachedQuestion.model_name, CachedQuestion.hit_count)
        .order_by(CachedQuestion.hit_count.desc())
        .limit(8)
        .all()
    )
    print(results)
    result = []
    for r in results:
        if r.name:
            result.append({"type": r.type, "name": r.name,"model_name" : r.model_name, "hits": r.hit_count})
    return result
