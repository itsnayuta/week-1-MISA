from fastapi import FastAPI
from pydantic import BaseModel
from agent import TOOLS, tools
import google.generativeai as genai

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

# Khởi tạo model và chat session 1 lần 
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=tools,
)
chat = model.start_chat(enable_automatic_function_calling=False)

def agent_handle(user_input: str) -> str:
    response = chat.send_message(user_input)
    if response.candidates and response.candidates[0].content.parts:
        parts = response.candidates[0].content.parts
        part = parts[0]
        if hasattr(part, 'function_call'):
            fn_call = part.function_call
            fn_name = fn_call.name
            fn_args = fn_call.args
            if fn_name in TOOLS:
                result = TOOLS[fn_name](**fn_args)
                followup = chat.send_message(f"Kết quả của hàm {fn_name}: {result}")
                return followup.text
            else:
                return f"Không tìm thấy hàm {fn_name}"
        else:
            return response.text
    else:
        return response.text

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    result = agent_handle(req.message)
    return {"response": result}