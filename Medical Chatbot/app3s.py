import streamlit as st
import app3
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. UI Configuration ---
st.set_page_config(page_title="Medical Assistant", page_icon="🩺")
st.title("🩺 Medical AI Chatbot")
st.caption("Ask your medical queries below. I'll process them using the backend logic.")


# --- 2. Backend Logic ---
def handle_logic(user_input, chat_history):
    """
    Calls the RAG chain and passes the required 'chat_history' variable.
    """
    # FIX: We now pass both 'input' and 'chat_history'
    response = app3.rag_chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return response['answer']


# --- 3. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []  # Used for Streamlit UI display

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Used for LLM Memory (LangChain objects)

# --- 4. Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. User Input & Interaction ---
if prompt := st.chat_input("Type your medical question here..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get AI Response
    with st.chat_message("assistant"):
        # We pass the prompt and the current chat_history list
        response_text = handle_logic(prompt, st.session_state.chat_history)
        st.markdown(response_text)

    # 3. Update History for UI
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # 4. Update History for LLM (This makes it remember previous questions)
    st.session_state.chat_history.extend([
        HumanMessage(content=prompt),
        AIMessage(content=response_text)
    ])