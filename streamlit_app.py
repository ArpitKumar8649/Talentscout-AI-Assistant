"""
TalentScout AI Hiring Assistant - Phase 2 with Letta Integration
Streaming responses with real-time display
"""
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import sys
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv('.env.streamlit')

from config.settings import settings
from utils.constants import ConversationStage, REQUIRED_FIELDS
from utils.helpers import is_exit_keyword
from services.letta_service import letta_service

# Page configuration
st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.app_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - ChatGPT Style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main App Background - Clean White */
    .stApp {
        background: #ffffff;
    }
    
    /* Main Content Area */
    section[data-testid="stAppViewContainer"] {
        background: #ffffff;
        padding-top: 0 !important;
    }
    
    /* Header Container */
    .main-header {
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        color: #202123;
        letter-spacing: -0.3px;
    }
    
    .sub-header {
        font-size: 0.875rem;
        color: #6e6e80;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    /* Chat Messages - ChatGPT Style */
    .stChatMessage {
        border-radius: 0 !important;
        padding: 1.5rem 1rem !important;
        margin: 0 !important;
        border-bottom: 1px solid #f7f7f8 !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    
    /* User Message Styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background-color: #ffffff !important;
    }
    
    /* Assistant Message Styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: #f7f7f8 !important;
    }
    
    /* Chat Message Content */
    .stChatMessage p {
        color: #374151 !important;
        font-size: 1rem;
        line-height: 1.75;
        font-weight: 400;
    }
    
    /* Force all text in messages to be visible */
    .stChatMessage div,
    .stChatMessage span,
    .stChatMessage p,
    .stChatMessage a {
        color: #374151 !important;
    }
    
    /* Override any inherited styles */
    [data-testid="stChatMessage"] * {
        color: #374151 !important;
    }
    
    /* Ensure markdown content is visible */
    .stMarkdown {
        color: #374151 !important;
    }
    
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span {
        color: #374151 !important;
    }
    
    /* Avatar Styling */
    [data-testid="chatAvatarIcon-user"] {
        background: #19c37d !important;
    }
    
    [data-testid="chatAvatarIcon-assistant"] {
        background: #ab68ff !important;
    }
    
    /* Sidebar Styling - Dark Mode */
    [data-testid="stSidebar"] {
        background: #202123;
        border-right: 1px solid #2d2d30;
    }
    
    [data-testid="stSidebar"] * {
        color: #ececf1 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff !important;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #4d4d4f;
    }
    
    /* Info Cards in Sidebar */
    .info-card {
        background: #2d2d30;
        border-radius: 8px;
        padding: 0.875rem;
        margin: 0.75rem 0;
        border: 1px solid #4d4d4f;
    }
    
    .info-label {
        font-size: 0.75rem;
        color: #8e8ea0 !important;
        font-weight: 500;
        margin-bottom: 0.375rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .info-value {
        font-size: 0.875rem;
        color: #ececf1 !important;
        font-weight: 400;
    }
    
    /* Connection Status Badge */
    .connection-status {
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.75rem 0;
        font-size: 0.875rem;
    }
    
    .status-connected {
        background: #1a7f5a;
        border: 1px solid #2d9d6e;
        color: #d1fae5 !important;
    }
    
    .status-error {
        background: #8b1e1e;
        border: 1px solid #dc2626;
        color: #fee2e2 !important;
    }
    
    /* Reasoning Message - Subtle Italic */
    .reasoning-message {
        font-style: italic;
        color: #6e6e80;
        background: #f7f7f8;
        padding: 0.875rem 1rem;
        border-radius: 6px;
        border-left: 3px solid #d1d5db;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .reasoning-message em {
        font-style: italic;
        color: #6e6e80;
    }
    
    /* Tool Call Badge */
    .tool-call {
        background: #eff6ff;
        padding: 0.625rem 0.875rem;
        border-radius: 6px;
        border-left: 3px solid #3b82f6;
        margin: 0.5rem 0;
        font-size: 0.875rem;
        color: #1e40af;
    }
    
    /* Chat Input Styling */
    .stChatInputContainer {
        border-top: 1px solid #f7f7f8;
        padding: 1rem 0;
    }
    
    /* Button Styling */
    .stButton button {
        background: #10a37f;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background: #1a7f5a;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ececf1 !important;
        font-size: 1.5rem !important;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'letta_connected' not in st.session_state:
        st.session_state.letta_connected = False
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    if 'current_reasoning' not in st.session_state:
        st.session_state.current_reasoning = ""
    
    if 'current_assistant' not in st.session_state:
        st.session_state.current_assistant = ""
    
    if 'agent_info' not in st.session_state:
        st.session_state.agent_info = None


def connect_to_letta():
    """Connect to Letta service"""
    if not st.session_state.letta_connected:
        with st.spinner("Connecting to Letta Agent..."):
            success = letta_service.connect()
            if success:
                st.session_state.letta_connected = True
                st.session_state.agent_info = letta_service.get_agent_info()
                return True
            else:
                st.error("❌ Failed to connect to Letta Agent. Check your credentials.")
                return False
    return True


def render_sidebar():
    """Render sidebar - ChatGPT style"""
    with st.sidebar:
        st.markdown('<p class="sidebar-header">🤖 Agent Status</p>', unsafe_allow_html=True)
        
        # Connection status
        if st.session_state.letta_connected:
            st.markdown("""
            <div class="connection-status status-connected">
                <strong>✓ AI Agent Connected</strong>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.agent_info:
                info = st.session_state.agent_info
                st.markdown(f"""
                <div class="info-card">
                    <p class="info-label">Agent ID</p>
                    <p class="info-value" style="font-size: 0.75rem; word-break: break-all;">{info.get('id', 'N/A')[:36]}...</p>
                </div>
                <div class="info-card">
                    <p class="info-label">Model</p>
                    <p class="info-value">{info.get('model', 'N/A')}</p>
                </div>
                <div class="info-card">
                    <p class="info-label">Agent Name</p>
                    <p class="info-value">{info.get('name', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="connection-status status-error">
                <strong>⚠ Connection Error</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.5rem 0; border-top: 1px solid #4d4d4f;"></div>', unsafe_allow_html=True)
        
        # Conversation stats
        st.markdown('<p class="sidebar-header">💬 Conversation</p>', unsafe_allow_html=True)
        message_count = len([m for m in st.session_state.messages if m.get('role') == 'user'])
        st.metric("Messages Sent", message_count)
        
        st.markdown('<div style="margin: 1.5rem 0; border-top: 1px solid #4d4d4f;"></div>', unsafe_allow_html=True)
        
        # About section
        st.markdown('<p class="sidebar-header">ℹ️ Capabilities</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.875rem; line-height: 1.6; color: #ececf1;">
        • Candidate information gathering<br>
        • Technical skills assessment<br>
        • Context-aware conversations<br>
        • Real-time streaming responses
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.5rem 0; border-top: 1px solid #4d4d4f;"></div>', unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 New Conversation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_message(message):
    """Render a single message - for historical display"""
    role = message.get('role')
    content = message.get('content', '')
    
    if role == 'user':
        with st.chat_message("user"):
            st.write(content)
    
    elif role == 'assistant':
        # For historical messages, show reasoning in italic ONLY if present
        # Reasoning was already shown during streaming, so we include it here
        # for completeness when scrolling through history
        if message.get('reasoning') and message['reasoning'].strip():
            st.markdown(f"""
            <div class="reasoning-message">
                <em>💭 {message['reasoning']}</em>
            </div>
            """, unsafe_allow_html=True)
        
        # Show ONLY assistant message content - NO reasoning text mixed in
        if content and content.strip():
            with st.chat_message("assistant"):
                st.write(content)
        
        # Show tool calls if present
        if message.get('tool_calls') and len(message['tool_calls']) > 0:
            for tool_call in message['tool_calls']:
                st.markdown(f"""
                <div class="tool-call">
                    🔧 <strong>Tool:</strong> {tool_call}
                </div>
                """, unsafe_allow_html=True)


def handle_stream_response(user_message: str):
    """Handle streaming response from Letta"""
    try:
        # Track message components - keep reasoning and assistant SEPARATE
        reasoning_parts = {}
        assistant_parts = {}
        tool_calls = []
        
        # Create placeholders for streaming
        reasoning_container = st.empty()
        assistant_container = st.empty()
        
        # Stream responses
        for chunk in letta_service.send_message_stream(user_message, stream_tokens=True):
            chunk_type = chunk.get('type')
            
            if chunk_type == 'reasoning':
                # Accumulate reasoning - keep SEPARATE from assistant
                msg_id = chunk.get('message_id', 'default')
                content = chunk.get('content', '')
                reasoning_parts[msg_id] = content
                
                # Display reasoning in italic ONLY - separate from message
                full_reasoning = ' '.join(reasoning_parts.values())
                if full_reasoning.strip():
                    reasoning_container.markdown(f"""
                    <div class="reasoning-message">
                        <em>💭 {full_reasoning}</em>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif chunk_type == 'assistant':
                # Accumulate assistant message
                msg_id = chunk.get('message_id', 'default')
                content = chunk.get('content', '')
                assistant_parts[msg_id] = content
                
                # Get full texts
                full_reasoning = ' '.join(reasoning_parts.values()).strip()
                full_assistant = ' '.join(assistant_parts.values()).strip()
                
                # CORE FIX: Remove reasoning text from assistant message if it's duplicated
                # Letta includes reasoning in assistant message, we need to extract only the response
                if full_reasoning and full_assistant.startswith(full_reasoning):
                    # Remove the reasoning part from assistant message
                    clean_assistant = full_assistant[len(full_reasoning):].strip()
                else:
                    clean_assistant = full_assistant
                
                # Display ONLY clean assistant message - without reasoning
                if clean_assistant:
                    with assistant_container:
                        with st.chat_message("assistant"):
                            st.write(clean_assistant)
            
            elif chunk_type == 'tool_call':
                tool_name = chunk.get('tool_name', 'unknown')
                tool_calls.append(tool_name)
                st.markdown(f"""
                <div class="tool-call">
                    🔧 <strong>Calling tool:</strong> {tool_name}
                </div>
                """, unsafe_allow_html=True)
            
            elif chunk_type == 'error':
                st.error(f"❌ {chunk.get('content', 'Unknown error')}")
                return None
        
        # Store complete message with reasoning removed from assistant content
        full_reasoning = ' '.join(reasoning_parts.values()).strip()
        full_assistant = ' '.join(assistant_parts.values()).strip()
        
        # Remove reasoning from assistant content if duplicated
        if full_reasoning and full_assistant.startswith(full_reasoning):
            clean_assistant = full_assistant[len(full_reasoning):].strip()
        else:
            clean_assistant = full_assistant
        
        # Return message with ONLY clean assistant content
        return {
            'role': 'assistant',
            'content': clean_assistant,  # Clean assistant message WITHOUT reasoning
            'reasoning': '',  # Don't store reasoning to avoid duplication on rerun
            'tool_calls': tool_calls
        }
    
    except Exception as e:
        st.error(f"❌ Error during streaming: {str(e)}")
        return None


def main():
    """Main application"""
    
    # Initialize
    initialize_session_state()
    
    # Header - ChatGPT Style
    st.markdown(
        f'<h1 class="main-header">{settings.app_title}</h1>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">AI-Powered Hiring Assistant with Real-Time Streaming</p>',
        unsafe_allow_html=True
    )
    
    # Connect to Letta
    if not st.session_state.letta_connected:
        connect_to_letta()
    
    # Render sidebar
    render_sidebar()
    
    # Main chat interface - no subtitle for cleaner look
    
    # Display chat history
    for message in st.session_state.messages:
        render_message(message)
    
    # Chat input
    if st.session_state.letta_connected:
        if prompt := st.chat_input("Type your message here...", key="user_input"):
            # Add user message to history
            st.session_state.messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Get streaming response (this will display reasoning and assistant message)
            response = handle_stream_response(prompt)
            
            # Store the response WITHOUT reasoning to avoid duplication
            # Reasoning was already displayed during streaming
            if response:
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': response['content'],  # Only store assistant content
                    'reasoning': '',  # Don't store reasoning to avoid showing twice
                    'tool_calls': response.get('tool_calls', [])
                })
            
            # Rerun to update chat history
            st.rerun()
    else:
        st.warning("⚠️ Please wait for Letta connection to be established.")


if __name__ == "__main__":
    main()
