from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from APP.code.agent_ai import get_response_from_ai_agents
from APP.config.settings import settings
from APP.common.log import get_logger
from APP.common.exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request for model : {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400 , detail="Invalid model name")
    
    try:
        response = get_response_from_ai_agents(
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Sucesfully got response from AI Agent {request.model_name}")

        return {"response" : response}
    
    except Exception as e:
        logger.exception("Error during response generation")
        raise HTTPException(
            status_code=500 , 
            detail=str(CustomException("Failed to get AI response" , error_detail=e))
            )
        
'''
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, AsyncGenerator
from APP.code.agent_ai import get_response_from_ai_agents
from APP.config.settings import settings
from APP.common.log import get_logger
from APP.common.exception import CustomException

logger = get_logger(__name__)
app = FastAPI(title="MULTI AI AGENT")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

@app.post("/chat")
async def chat_endpoint(request: RequestState):
    """
    Async endpoint to handle long-running Bedrock + Tavily tasks 
    without triggering connection resets.
    """
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model name")

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            # Note: Ensure get_response_from_ai_agents is updated to be async 
            # or wrapped in run_in_threadpool if it's strictly synchronous
            response = await get_response_from_ai_agents(
                request.model_name,
                request.messages,
                request.allow_search,
                request.system_prompt
            )
            
            # Send the final response as a JSON string
            yield json.dumps({"response": response})
            
        except Exception as e:
            logger.error(f"Error during response generation: {str(e)}")
            yield json.dumps({"error": "Failed to get AI response", "details": str(e)})

    return StreamingResponse(event_generator(), media_type="application/json")

# Run with increased timeout: 
# uvicorn main:app --timeout-keep-alive 120 --workers 1'''
