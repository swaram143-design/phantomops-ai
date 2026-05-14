import streamlit as st
from langchain_ollama import OllamaLLM
from memory.memory_manager import load_memory, save_memory

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="JARVIS AI",
    layout="wide"
)

# -----------------------------
# HIDE STREAMLIT UI ELEMENTS
# -----------------------------

hide_streamlit_style = """
<style>
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}
</style>
"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)

# -----------------------------
# LOAD AI MODEL
# -----------------------------

llm = OllamaLLM(
    model="phi3",
    temperature=0.3
)

# -----------------------------
# TITLE
# -----------------------------

st.title("🤖 JARVIS AI ASSISTANT")

# -----------------------------
# LOAD MEMORY
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = load_memory()

# -----------------------------
# DISPLAY OLD CHAT
# -----------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------

prompt = st.chat_input("Talk to JARVIS...")

# -----------------------------
# PROCESS INPUT
# -----------------------------

if prompt:

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # -----------------------------
    # BUILD CONVERSATION HISTORY
    # -----------------------------

    conversation_history = ""

    for msg in st.session_state.messages[-6:]:

        role = msg["role"]
        content = msg["content"]

        conversation_history += f"{role}: {content}\n"

    # -----------------------------
    # SYSTEM PROMPT
    # -----------------------------

    full_prompt = f"""
You are JARVIS, a futuristic AI assistant.

Rules:
- Your name is JARVIS.
- Never say you are Phi.
- Never mention Microsoft.
- Remember previous conversation context.
- Give short intelligent responses.
- Be professional and futuristic.

Conversation History:
{conversation_history}

Current User Message:
{prompt}

JARVIS:
"""

    # -----------------------------
    # GENERATE RESPONSE
    # -----------------------------

    with st.spinner("⚡ JARVIS Processing..."):

        response = llm.invoke(full_prompt)

    # -----------------------------
    # DISPLAY RESPONSE
    # -----------------------------

    with st.chat_message("assistant"):

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # -----------------------------
    # SAVE MEMORY
    # -----------------------------

    save_memory(st.session_state.messages)