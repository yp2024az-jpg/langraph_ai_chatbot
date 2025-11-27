import streamlit as st
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from chatbot_backed import chatbot
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def generate_thread_id():
    return str(uuid.uuid4())
def add_thread(thread_id: str):
    # ensure chat_threads exists and append if missing
    if 'chat_threads' not in st.session_state:
        st.session_state['chat_threads'] = []
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    # set active thread id and create a new empty message history
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages',[])
# Initialize session state keys safely
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    # ensure the initial thread is tracked
    add_thread(st.session_state['thread_id'])
st.sidebar.text("Langgraph chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header('My Conversations')
# iterate safely over chat_threads (may be empty)
for thread_id in st.session_state.get('chat_threads', [])[::-1]:
    # create a button per thread; when pressed load that conversation
    st.session_state['thread_id'] = thread_id
    messages = load_conversation(thread_id)
    if messages!=[]:
        conversation1=model.invoke(f"give a meaningfull title to this conversation {messages}")
    if messages==[]:
        conversation1='new_chat'
    if st.sidebar.button(str(conversation1)):

        temp_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages

message_history=[]
for message in st.session_state["message_history"]:
     with st.chat_message(message["role"]):
         st.text(message['content'])

CONFIG={'configurable':{'thread_id':st.session_state["thread_id"]}}
user_input = st.chat_input("")
if user_input:
     st.session_state["message_history"].append({"role": "user", "content": user_input})
     with st.chat_message("user"):
         st.text(user_input)
     
     
     with st.chat_message("assistant"):
          ai_message = st.write_stream(
                message_chunk.content for message_chunk, metadata in chatbot.stream(
                    
                    {'messages': [HumanMessage(content=user_input)]},
                    config= CONFIG,
                    stream_mode= 'messages'
            )
        )
     st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
     