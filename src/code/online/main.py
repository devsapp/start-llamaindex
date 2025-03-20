# -*- coding: utf-8 -*-
import uvicorn
import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from chat import *

app = FastAPI()


@app.post("/initialize")
def init():
    initializer()


# Return success to options
@app.options("/chat/completions")
@app.options("/v1/chat/completions")
async def root():
    return {"message": "success"}


@app.post("/chat/completions")
@app.post("/v1/chat/completions")
def chat_completion(
        req: ChatCompletionRequest,
):
    # TODO temprature 从这里获取
    messages = req.messages
    stream_gen = chat(req.messages[-1].content, [message.to_llamaindex_message() for message in messages])
    return StreamingResponse(stream_gen, media_type="text/event-stream")


@app.get("/models")
def get_models():
    return {
        "object": "list",
        "data": [{
            "id": os.getenv("OLLAMA_LLM_MODEL", "cap-deepseek-r1"),
            "object": "model"
        }]
    }


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
