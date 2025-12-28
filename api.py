import os   
import sys 
import uvicorn
from fastapi import FastAPI,HTTPException 
from pydantic import BaseModel 
from langchain_core.messages import AIMessage , HumanMessage
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
from core.graph import app_graph 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Smart Dental Bot API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sessions = {}
class UserRequest(BaseModel):
    query: str 
    session_id: str 

@app.get("/")
def home():
    """
    Root endpoint to check if the server is running (Health Check).
    This is accessible directly in the browser to verify the API status.
    """
    return {"status": "Online", "message": "Dental Bot Server is running! 🚀"}

@app.post("/chat") 
def chat_endpoint(request: UserRequest): 
    try:
        user_input = request.query 
        session_id = request.session_id 
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(HumanMessage(content=user_input))
        print(f"📩 Received form {session_id}: {user_input}")
        result = app_graph.invoke({"messages": sessions[session_id]})
        sessions[session_id] = result["messages"]
        bot_response = result["messages"][-1].content
        print(f"📤 Sent: {bot_response}")
        return {
            "response": bot_response,
            "status": "success"
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    print("Server starting on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)