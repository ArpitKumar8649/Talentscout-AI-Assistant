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

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .stChatMessage {
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.8rem 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    .info-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    
    .info-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        font-size: 1rem;
        color: #1e293b;
        font-weight: 500;
    }
    
    .progress-container {
        width: 100%;
        height: 12px;
        background: #e2e8f0;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 6px;
        transition: width 0.5s ease;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.3rem;
    }
    
    .badge-pending {
        background: #fef3c7;
        color: #92400e;
    }
    
    .reasoning-message {
        font-style: italic;
        color: #6b7280;
        background: #f9fafb;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border-left: 3px solid #9ca3af;
        margin: 0.5rem 0 1rem 0;
        font-size: 0.95rem;
    }
    
    .reasoning-message em {
        font-style: italic;
    }
    
    .assistant-message {
        color: #1f2937;
        line-height: 1.6;
    }
    
    .tool-call {
        background: #dbeafe;
        padding: 0.6rem;
        border-radius: 8px;
        border-left: 3px solid #3b82f6;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .connection-status {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-connected {
        background: #d1fae5;
        border: 1px solid #10b981;
        color: #065f46;
    }
    
    .status-error {
        background: #fee2e2;
        border: 1px solid #ef4444;
        color: #991b1b;
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
    """Render sidebar"""
    with st.sidebar:
        st.markdown('<p class="sidebar-header">📋 Agent Status</p>', unsafe_allow_html=True)
        
        # Connection status
        if st.session_state.letta_connected:
            st.markdown("""
            <div class="connection-status status-connected">
                <strong>✅ Letta Agent Connected</strong>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.agent_info:
                info = st.session_state.agent_info
                st.markdown(f"""
                <div class="info-card">
                    <p class="info-label">Agent ID</p>
                    <p class="info-value" style="font-size: 0.85rem;">{info.get('id', 'N/A')}</p>
                </div>
                <div class="info-card">
                    <p class="info-label">Model</p>
                    <p class="info-value">{info.get('model', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="connection-status status-error">
                <strong>⚠️ Not Connected</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Conversation stats
        st.subheader("💬 Conversation Stats")
        message_count = len([m for m in st.session_state.messages if m.get('role') == 'user'])
        st.metric("Messages Sent", message_count)
        
        st.markdown("---")
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        This AI hiring assistant:
        - 📝 Collects candidate information
        - 💻 Assesses technical skills  
        - 🎯 Generates relevant questions
        - 🤖 Uses Letta for stateful memory
        """)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset Conversation", use_container_width=True):
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
    
    # Header
    st.markdown(
        f'<h1 class="main-header">{settings.app_icon} {settings.app_title}</h1>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">Powered by Letta Agent Framework with Streaming 🚀</p>',
        unsafe_allow_html=True
    )
    st.markdown('---')
    
    # Connect to Letta
    if not st.session_state.letta_connected:
        connect_to_letta()
    
    # Render sidebar
    render_sidebar()
    
    # Main chat interface
    st.subheader("💬 Chat Interface")
    
    # Display chat history
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>👋 Welcome to TalentScout AI!</h3>
            <p style="font-size: 1.1rem; margin: 1rem 0;">
                I'm an AI hiring assistant powered by Letta. I'll help screen candidates by:
            </p>
            <ul style="font-size: 1rem; line-height: 1.8;">
                <li>📝 Collecting essential information</li>
                <li>💻 Understanding technical expertise</li>
                <li>🎯 Asking relevant questions</li>
                <li>🧠 Remembering context throughout our conversation</li>
            </ul>
            <p style="font-size: 1.1rem; margin-top: 1.5rem;">
                <strong>✨ Ready to begin? Just type your message below!</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
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
