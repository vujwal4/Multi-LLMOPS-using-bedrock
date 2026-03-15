from fastapi import FastAPI, Request
import traceback
from langchain_aws import ChatBedrock

app = FastAPI()

# Create LLM
llm = ChatBedrock(
    model_id="amazon.nova-lite-v1:0",
    region_name="us-east-1"
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")

        print("Incoming message:", message)

        response = llm.invoke(message)

        return {"response": str(response)}

    except Exception as e:
        print("ERROR OCCURRED")
        traceback.print_exc()
        return {"error": str(e)}