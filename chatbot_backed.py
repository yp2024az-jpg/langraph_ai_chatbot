from langgraph.graph import StateGraph, START,END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated,Literal,TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class bot_message(TypedDict):
    message: Annotated[list[str],add_messages]

def chat_node(state:bot_message):
    message=state["message"]
    response=model.invoke(message)
    return {'message':[response]}




checkpointer=InMemorySaver()
graph=StateGraph(bot_message)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)
