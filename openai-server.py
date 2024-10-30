from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse  # Updated import
from pydantic import BaseModel
from juchats.chat import Juchats
import time
import json
import asyncio
from loguru import logger

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list
    temperature: float = 0.7
    max_tokens: int = 64
    top_p: float = 1
    stream: bool = True


@app.post("/v1/chat/completions")
async def chat_completion(request: Request, chat_request: ChatCompletionRequest):
    try:
        api_key = request.headers.get(
            'Authorization', '').replace('Bearer ', '')
        if not api_key:
            raise HTTPException(status_code=401, detail="Missing API key")

        juchats = Juchats(api_key, model=chat_request.model)
        logger.info(f"Received request: {chat_request}")

        user_message = [msg['content']
                        for msg in chat_request.messages if msg['role'] == 'user'].pop()
        prompt = f"{user_message}"
        logger.info(f"inputing prompt: {prompt}")

        if chat_request.stream:
            async def event_generator():
                try:
                    async for chunk in juchats.stream_chat(prompt):
                        yield f"data: {json.dumps(format_chunk(chunk, chat_request))}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    error_message = f"Error during streaming: {str(e)}"
                    logger.error(error_message)
                    yield f"data: {json.dumps({'error': error_message})}\n\n"

            return StreamingResponse(event_generator(), media_type="text/event-stream")
        else:
            async with juchats:
                response = await juchats.chat(prompt)

            return format_non_stream_response(response, chat_request)

    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


def format_chunk(chunk, chat_request):
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": chat_request.model,  # Use the model from the request
        "choices": [
            {
                "index": 0,
                "delta": {
                    "content": chunk
                },
                "finish_reason": None
            }
        ]
    }


def format_non_stream_response(response, chat_request):
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": response,
                    "role": "assistant"
                },
                "logprobs": None
            }
        ],
        "created": int(time.time()),
        "id": f"chatcmpl-{int(time.time())}",
        "model": chat_request.model,
        "object": "chat.completion",
        "usage": {
            # This is a rough estimate
            "completion_tokens": len(response.split()),
            # This is a rough estimate
            "prompt_tokens": len(chat_request.messages[-1]['content'].split()),
            # This is a rough estimate
            "total_tokens": len(response.split()) + len(chat_request.messages[-1]['content'].split())
        }
    }


@app.get("/v1/models")
async def get_models(request: Request):
    api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    juchats = Juchats(api_key)
    async with juchats:
        models = await juchats.get_models()

    formatted_models = []
    for model in models:
        formatted_model = {
            "id": model.name,
            "object": "model",
            "created": 1686935002,  # Using a fixed timestamp as in the original
            "owned_by": "organization-owner",
            "type": model.id,
            "name": model.name,
            "showName": model.showName,
            "maxToken": model.maxToken,
            "searchFlag": 0,
            "remark": model.remark
        }
        formatted_models.append(formatted_model)

    return {
        "object": "list",
        "data": formatted_models
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
