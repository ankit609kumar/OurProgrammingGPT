import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables and configure page
load_dotenv()
st.set_page_config(
    page_title="Programming Assistant",
    page_icon="💻",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stMarkdown {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq_client()

# Title and description
st.title("💻 Programming Assistant")
st.markdown("""
This AI-powered programming assistant can help you with:
- Code explanations
- Debugging assistance
- Best practices
- Programming concepts
- And more!
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your programming question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with a loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create system message and user query
                messages = [
                    {
                        "role": "system",
                        "content": "You are a programming expert. Your task is to provide helpful, accurate answers to programming-related questions. For any non-programming questions, simply respond with 'I don't know!'."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                
                # Get response from Groq
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar with additional information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This is a Streamlit-powered interface for the Programming Assistant.
    
    *Features:*
    - Real-time responses
    - Chat history
    - Code formatting
    - Error handling
    
    *Model:* LLaMA 3.3 70B (via Groq)
    """)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()