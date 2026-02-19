from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama

app = FastAPI()



class Request(BaseModel):
    prompt: str
    model: str


ALLOWED_MODELS = {
    "phi3.5:3.8b-mini-instruct-q8_0",
    "phi3.5:3.8b-mini-instruct-q4_K_M",
    "phi3.5:3.8b-mini-instruct-q2_K"
}    
    

@app.post("/generate")
async def generate(request:Request):
    prompt = request.prompt
    model = request.model
    
    if not prompt:
        raise HTTPException(status_code=400, detail={
            "status_code": 400,
            "error": "Prompt cannot be empty"
        })
        
    if not model:
        raise HTTPException(status_code=400, detail={
            "status_code": 400,
            "error": "model cannot be empty"
        })
    
    if model not in ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail={
            "status_code": 400,
            "error": f"Model '{model}' is not allowed"
        })
        
    
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    
    latency = response.total_duration / 1_000_000_000
    eval_duration = response.eval_duration / 1_000_000_000
    tokens_per_second = response.eval_count / eval_duration
    
    return {
        "model": model,
        "response": response.message.content,
        "latency" : round(latency,2),
        "tokens_per_second": round(tokens_per_second,2),
    }
    