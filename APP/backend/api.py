from fastapi import FastAPI, Request
import traceback

app = FastAPI()

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