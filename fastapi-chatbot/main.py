from fastapi import FastAPI, WebSocket, Form, Request, Response
from typing import List, Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables once, at the start of the script.
load_dotenv()

# Initialize API keys and clients.
api_key = os.getenv('OPENAI_API_KEY')
sync_openai_client = OpenAI(api_key=api_key)
async_openai_client = AsyncOpenAI(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Use a list to store chat responses. Consider using a more scalable storage solution for production.
chat_responses: List[str] = []

# Initialize a chat log with a system message.
chat_log = [{
    'role': 'system',
    'content': ('You are a Helpful assistant, skilled in explaining complex concepts in simple terms. ')
}]


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Serve the chat page."""
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    """Handle user input from the chat form."""
    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    response = sync_openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        temperature=0.6
    )

    bot_response = response.choices[0].message.content
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket endpoint for real-time AI responses."""
    await websocket.accept()
    while True:
        user_message = await websocket.receive_text()
        async for ai_response in get_ai_response(user_message):
            await websocket.send_text(ai_response)


async def get_ai_response(message: str):
    """Generate responses from the AI asynchronously."""
    response = await async_openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, skilled in explaining complex concepts in simple terms."},
            {"role": "user", "content": message},
        ],
        stream=True,
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
