import os
import sys
import datetime
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)
import operator
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from modules.booking import check_availability, book_appointment
from modules.rag_faq import lookup_policy_faq
load_dotenv(os.path.join(parent_dir, '.env'))

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]


tools = [lookup_policy_faq, check_availability, book_appointment]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

BASE_SYSTEM_PROMPT = """
You are the AI Receptionist for 'Smart Care Dental Clinic'.
Your name is 'SmartBot'.

YOUR RESPONSIBILITIES:
1.  **General Info:** If the user asks about prices, location, or timings -> Use the 'lookup_policy_faq' tool.
2.  **Availability:** If the user asks for a slot (e.g., "Is 5 PM free tomorrow?") -> Use the 'check_availability' tool.
3.  **Booking:** If the user confirms an appointment (e.g., "Book it") -> Use the 'book_appointment' tool.

GUIDELINES:
-   **Language:** Always respond in a **Polite Roman Urdu + English Mix**. (Example: "Jee, main check karta hoon").
-   **FAQ Handling:** The tool might return 3-4 lines of data. You must extract and mention *only* the specific line the user asked for. Do not list everything.
-   **Context Understanding:** If the user says "Daant Safai", understand that they are referring to "Scaling".
-   **Clarification:** If you do not understand the user's query, politely ask them to clarify.
-   **Date Format:** ALWAYS use the `YYYY-MM-DD` format for the 'check_availability' and 'book_appointment' tools.

EXAMPLE:
User: "Scaling fees?"
Tool Data: "- Scaling: 3000, - RCT: 8000"
You: "Jee, Scaling ki fees 3000 PKR hai."
"""

def chatbot_node(state: AgentState):
    """
    Yeh function decide karta hai ke kya bolna hai ya kya tool use karna hai.
    """
    messages = state["messages"]
    
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d (%A)") 
    final_prompt = f"""{BASE_SYSTEM_PROMPT}

    🚨 CURRENT DATE & TIME SETTINGS:
    - Current Date (Today): {today_str}
    - If the user says Today, use the date: "{today.strftime('%Y-%m-%d')}".
    - If the user says Tomorrow, calculate the date as Today + 1 day.
    - If the user says Day after tomorrow, calculate the date as Today + 2 days.
    - IMPORTANT: Always perform the calculation yourself and send the specific date in 'YYYY-MM-DD' format to the tool.
    """
    if not isinstance(messages[0], SystemMessage):
        messages.insert(0, SystemMessage(content=final_prompt))
    else: 
        messages[0] = SystemMessage(content=final_prompt)
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """
    This function acts as a Router/Traffic Controller.
    - If the AI requests a Tool -> Route to the 'tools' node.
    - If the AI provides a final answer -> Route to END (respond to the user).
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("agent", chatbot_node)
workflow.add_node("tools", ToolNode(tools)) 
workflow.set_entry_point("agent") 
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END          
    }
)
workflow.add_edge("tools", "agent")
app_graph = workflow.compile()

if __name__ == "__main__":
    print("🤖 Bot Graph Ready! Testing...")
    user_input = "any question ask"
    result = app_graph.invoke({"messages": [HumanMessage(content=user_input)]})
    print(f"Bot: {result['messages'][-1].content}")