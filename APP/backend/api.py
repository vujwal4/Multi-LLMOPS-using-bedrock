from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from APP.code.agent_ai import get_response_from_ai_agents
from APP.config.settings import settings
from APP.common.log import get_logger

logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")


class RequestState(BaseModel):
    model_name: Optional[str] = "amazon.nova-lite-v1:0"
    system_prompt: Optional[str] = "You are a helpful AI assistant."
    messages: List[str]
    allow_search: Optional[bool] = False


@app.post("/chat")
async def chat_endpoint(request: RequestState):

    logger.info(f"Received request for model: {request.model_name}")

    # Validate model name
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model name. Allowed models: {settings.ALLOWED_MODEL_NAMES}"
        )

    # Validate messages
    if not request.messages:
        raise HTTPException(
            status_code=400,
            detail="Messages list cannot be empty"
        )

    try:
        # Call AI Agent
        response =await get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Successfully got response from AI Agent {request.model_name}")

        return {
            "status": "success",
            "response": response
        }

    except Exception as e:
        logger.exception("Error during response generation")

        raise HTTPException(
            status_code=500,
            detail=f"AI agent failed: {str(e)}"
        )